import logging

from asyncpg import UniqueViolationError
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import config
from linked_roles import LinkedRolesOAuth2, OAuth2Scopes, RoleConnection
from raiderio_async import RaiderIO

from models import GuildMember

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

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
        # role.add_metadata(key="class", value=player_character.spec_and_class)

        # set role metadata
        await user.edit_role_connection(role)

        # save data to db
        await GuildMember.create_table(if_not_exists=True)
        try:
            log.info(f"Inserting {character_name} into db")
            await GuildMember.insert(
                GuildMember(
                    user_id=str(user.id),
                    character_name=character_name,
                    guild_rank=str(player_character.guild_rank),
                    ilvl=str(player_character.ilvl),
                    score=str(player_character.score),
                    access_token=token.access_token,
                    refresh_token=token.refresh_token,
                    token_expires_at=str(token.expires_at.timestamp()),
                ),
            )
            log.info(f"Inserted {character_name} into db")
        except UniqueViolationError:
            log.info(f"Updating {character_name} in db")
            await GuildMember.update(
                user_id=str(user.id),
                character_name=character_name,
                guild_rank=str(player_character.guild_rank),
                ilvl=str(player_character.ilvl),
                score=str(player_character.score),
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                token_expires_at=str(token.expires_at.timestamp()),
            ).where(GuildMember.user_id == str(user.id)).run()
            log.info(f"Updated {character_name} in db")

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

        data = await cls.get_character_data(name)

        self.name = name
        self.ilvl = data["character"]["items"]["item_level_equipped"]
        self.score = data["keystoneScores"]["allScore"]
        # self.spec_and_class = f"{data['spec']['name']} {data['class']['name']}"
        self.guild_rank = data["rank"]

        return self

    @classmethod
    async def get_character_data(cls, name):
        async with RaiderIO() as rio:
            # This shouldn't be accessed every time, but we use caching, so it's probably ok
            guild_data = await rio.get_guild_roster("eu", "ragnaros", "Jahaci Rumene Kadulje")
        if data := next(
            (
                character
                for character in guild_data["guildRoster"]["roster"]
                if character["character"]["name"] == name
            ),
            None,
        ):
            return data
        else:
            raise CharacterNotFound("Character not found")


class CharacterNotFound(Exception):
    pass
