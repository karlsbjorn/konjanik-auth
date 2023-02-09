from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import config
from linked_roles import LinkedRolesOAuth2, OAuth2Scopes, RoleConnection
from raiderio_async import RaiderIO

app = FastAPI(title="Konjanik OAuth2")

client = LinkedRolesOAuth2(
    client_id=config.DISCORD_CLIENT_ID,
    client_secret=config.DISCORD_CLIENT_SECRET,
    redirect_uri=config.DISCORD_REDIRECT_URI,
    token=config.DISCORD_TOKEN,
    scopes=(OAuth2Scopes.role_connection_write, OAuth2Scopes.identify),
    state=config.COOKIE_SECRET,
)


@app.on_event("startup")
async def startup():
    await client.start()


@app.on_event("shutdown")
async def shutdown():
    await client.close()


@app.get("/linked-role")
async def linked_roles():
    url = client.get_oauth_url()
    return RedirectResponse(url=url)


@app.get("/verified-role")
async def verified_role(code: str):
    # get token
    token = await client.get_access_token(code)

    # get user
    user = await client.fetch_user(token)

    if int(user.id) in config.MEMBERS.keys():
        character_name = config.MEMBERS[int(user.id)]
        # set role connection
        role = RoleConnection(platform_name="World of Warcraft", platform_username=character_name)

        # get character data
        player_character = await PlayerCharacter().create(character_name)

        # add metadata
        if player_character.guild_rank in config.GUILD_RANKS.keys():
            role.add_metadata(key=config.GUILD_RANKS[player_character.guild_rank], value=True)
        role.add_metadata(key="ilvl", value=player_character.ilvl)
        role.add_metadata(key="mplusscore", value=int(player_character.score))
        #role.add_metadata(key="class", value=player_character.spec_and_class)

        # set role metadata
        await user.edit_role_connection(role)
        return (
            f"Sve je proslo ok. "
            f"Tvoj character je {character_name}. Provjeri svoj Discord profil."
        )
    return "Nisi autoriziran za ovu radnju. Kontaktiraj @Karlo"


class PlayerCharacter:
    name: str
    ilvl: int
    score: float
    spec_and_class: str
    guild_rank: int

    @classmethod
    async def create(cls, name: str):
        self = PlayerCharacter()
        async with RaiderIO() as rio:
            # This shouldn't be accessed every time, but we use caching, so it's probably ok
            guild_data = await rio.get_guild_roster("eu", "ragnaros", "Jahaci Rumene Kadulje")

        data = next(
            (
                character
                for character in guild_data["guildRoster"]["roster"]
                if character["character"]["name"] == name
            ),
            None,
        )
        if not data:
            raise CharacterNotFound("Character not found")
        self.name = name
        self.ilvl = data["character"]["items"]["item_level_equipped"]
        self.score = data["keystoneScores"]["allScore"]
        #self.spec_and_class = f"{data['spec']['name']} {data['class']['name']}"
        self.guild_rank = data["rank"]
        return self


class CharacterNotFound(Exception):
    pass
