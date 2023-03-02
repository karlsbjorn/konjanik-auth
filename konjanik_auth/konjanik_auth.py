import logging

import config
import sentry_sdk
from asyncpg import UniqueViolationError
from discord.ext import tasks
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from linked_roles import LinkedRolesOAuth2, OAuth2Scopes, RoleConnection
from linked_roles.oauth2 import OAuth2Token
from models import GuildMember
from playercharacter import PlayerCharacter
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    integrations=[
        FastApiIntegration(),
        LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        AioHttpIntegration(),
    ],
    traces_sample_rate=1.0,
)

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
    log.info("Starting update users task")
    UpdateUsers().update_users.start()


@app.on_event("shutdown")
async def shutdown():
    await client.close()
    log.info("Stopping update users task")
    UpdateUsers().update_users.stop()


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
            f"Sve je prošlo ok. "
            f"Tvoj character je {character_name}. Provjeri svoj Discord profil."
        )
    log.info(f"{user.id} tried to authenticate but is not in the list of members.")
    return "Nisi autoriziran za ovu radnju. Ako je ovo greška, kontaktiraj @Karlo"


class UpdateUsers:
    @tasks.loop(hours=1)
    async def update_users(self):
        log.info("Updating users")
        for member in await GuildMember.select():
            try:
                refreshed_token = await client._http.refresh_oauth2_token(member["refresh_token"])
            except Exception as e:
                log.warning(f"Error refreshing token for {member['character_name']}: {e}")
                continue
            token = OAuth2Token(client, refreshed_token)
            await GuildMember.update(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                token_expires_at=str(token.expires_at.timestamp()),
            ).where(GuildMember.user_id == str(member["user_id"])).run()

            user = await client.fetch_user(token)

            # log.info(f"{role.to_dict()}")  # debug

            name = config.MEMBERS[int(user.id)]
            player_character = await PlayerCharacter().create(name)

            role = RoleConnection(platform_name="Jahači Rumene Kadulje", platform_username=name)
            role.add_metadata(key="ilvl", value=int(member["ilvl"]))
            role.add_metadata(key="mplusscore", value=int(float(member["score"])))

            changes = await self.update_member_data(member, player_character, role, user)
            if not changes:
                continue

            try:
                await user.edit_role_connection(role)
                log.info(f"Updated user {name}")
            except (ValueError, TypeError):
                log.warning(f"Error updating user {name}", exc_info=True)

    @staticmethod
    async def update_member_data(member, player_character, role, user):
        changes = False

        if player_character.ilvl != int(member["ilvl"]):
            log.info(f"Updating {player_character.name} ilvl")
            await GuildMember.update(ilvl=str(player_character.ilvl)).where(
                GuildMember.user_id == str(user.id)
            ).run()
            role.add_or_edit_metadata(key="ilvl", value=int(player_character.ilvl))
            changes = True

        if player_character.score != float(member["score"]):
            log.info(f"Updating {player_character.name} score")
            await GuildMember.update(score=str(player_character.score)).where(
                GuildMember.user_id == str(user.id)
            ).run()
            role.add_or_edit_metadata(key="mplusscore", value=int(player_character.score))
            changes = True

        return changes

    @update_users.error
    async def update_users_error(self, error):
        log.error(f"Unhandled error in update_users: {error}", exc_info=True)
