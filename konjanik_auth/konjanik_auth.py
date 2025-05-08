import logging
import secrets
import time
import uuid
from urllib.parse import urlencode

import aiohttp
import sentry_sdk
from discord.ext import tasks
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from linked_roles import LinkedRolesOAuth2, OAuth2Scopes
from linked_roles.oauth2 import OAuth2Token
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from konjanik_auth import config
from konjanik_auth.models import BnetToken, DiscordToken, GuildMember

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
logging.getLogger("aiohttp_client_cache.backends.base").setLevel(logging.WARNING)

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
sessions: dict[str, dict] = {}  # probably use redis or something idk

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


def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authed")

    session_data = sessions[session_id]
    if session_data["expires_at"] < time.time():
        sessions.pop(session_id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    return session_data["discord_user_id"]


@app.get("/verified-role")
async def verified_role(response: Response, code: str):
    # get token
    token = await client.get_access_token(code)

    # get user
    user = await client.fetch_user(token)
    if not user:
        log.error("Failed to fetch user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = int(user.id)

    await DiscordToken.insert(
        DiscordToken(
            user_id=user_id,
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            expires_at=int(token.expires_at.timestamp()),
        )
    ).on_conflict(
        action="DO UPDATE",
        values=DiscordToken.all_columns(),
        target=DiscordToken.user_id,
    )

    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "discord_user_id": str(user_id),
        "created_at": time.time(),
        "expires_at": time.time() + 3600,
    }

    # Have user log into bnet as well
    response = RedirectResponse(url="/bnet-auth")
    response.set_cookie(
        key="session_id", value=session_id, httponly=True, secure=True, max_age=3600
    )
    return response


@app.get("/bnet-auth")
async def bnet_auth(discord_user_id: str = Depends(get_current_user)):
    """Initiate Battle.net OAuth flow"""
    anti_csrf = secrets.token_hex(16)
    for session_id, session_data in sessions.items():
        if session_data["discord_user_id"] == discord_user_id:
            session_data["anti_csrf"] = anti_csrf
            break

    params = {
        "client_id": config.BNET_CLIENT_ID,
        "redirect_uri": config.BNET_REDIRECT_URI,
        "response_type": "code",
        "scope": "wow.profile",
        "state": f"{discord_user_id}:{anti_csrf}",  # Pass Discord user ID as state for verification
    }

    auth_url = f"{config.BNET_AUTHORIZE_URL}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@app.get("/bnet-callback")
async def bnet_callback(
    request: Request,
    code: str,
    state: str,
):
    try:
        discord_user_id, anti_csrf = state.split(":")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state format."
        )

    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session invalid.")
    session_data = sessions[session_id]
    if session_data["discord_user_id"] != discord_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session verification failed."
        )
    if session_data.get("anti_csrf") != anti_csrf:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="CSRF failure.")
    sessions.pop(session_id)

    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(config.BNET_CLIENT_ID, config.BNET_CLIENT_SECRET)
        async with session.post(
            config.BNET_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": config.BNET_REDIRECT_URI,
            },
            auth=auth,
        ) as response:
            if response.status != 200:
                error_data = await response.text()
                log.error(f"Battle.net token error: {error_data}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to obtain Battle.net token.",
                )

            bnet_token_data = await response.json()

    await BnetToken.insert(
        BnetToken(
            user_id=int(discord_user_id),
            access_token=bnet_token_data["access_token"],
            token_type=bnet_token_data["token_type"],
            expires_at=int(time.time()) + bnet_token_data["expires_in"],
            scope=bnet_token_data["scope"],
            sub=bnet_token_data["sub"],  # bnet id
        )
    ).on_conflict(
        action="DO UPDATE",
        values=BnetToken.all_columns(),
        target=BnetToken.user_id,
    )

    await GuildMember.insert(
        GuildMember(
            user_id=int(discord_user_id),
            discord_token=int(discord_user_id),
            bnet_token=int(discord_user_id),
        )
    ).on_conflict(
        action="DO UPDATE",
        values=GuildMember.all_columns(),
        target=GuildMember.user_id,
    )

    async with aiohttp.ClientSession() as session:
        url = f"{config.BNET_API_URL}/profile/user/wow"
        headers = {"Authorization": f"Bearer {bnet_token_data['access_token']}"}
        params = {":region": "eu", "namespace": "profile-eu", "locale": "en_US"}
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                data = await response.json()
                log.error(f"Battle.net API error: {data}\n{url}\n{headers}")
            else:
                log.info(f"Fetched WoW profile for {discord_user_id}")

    return {
        "status": "success",
        "message": "Autorizacija uspjela.",
        "user_id": discord_user_id,
    }


# async def add_approved_user(token, user):
#     character_name = (
#         await AssignedCharacter.select(AssignedCharacter.character_name)
#         .where(AssignedCharacter.user_id == int(user.id))
#         .first()
#     ).get("character_name")

#     # get character data
#     player_character = await PlayerCharacter().create(character_name)

#     # set role connection
#     role = RoleConnection(
#         platform_name=player_character.full_class_name, platform_username=character_name
#     )

#     # add metadata
#     role.add_metadata(key="ilvl", value=player_character.ilvl)
#     role.add_metadata(key="mplusscore", value=int(player_character.score))
#     if player_character.guild_lb_position:
#         role.add_metadata(key="guildlbposition", value=player_character.guild_lb_position)
#     if player_character.guild_rank and player_character.guild_rank <= 3:
#         role.add_metadata(key="raider", value=True)

#         # set role metadata
#     await user.edit_role_connection(role)

#     # save data to db
#     await GuildMember.create_table(if_not_exists=True)
#     log.info(f"Inserting {character_name} into db")
#     await GuildMember.insert(
#         GuildMember(
#             user_id=str(user.id),
#             character_name=character_name,
#             guild_rank=str(player_character.guild_rank),
#             ilvl=str(player_character.ilvl),
#             score=str(player_character.score),
#             guild_lb_position=player_character.guild_lb_position,
#             access_token=token.access_token,
#             refresh_token=token.refresh_token,
#             token_expires_at=str(token.expires_at.timestamp()),
#         ),
#     ).on_conflict(
#         action="DO UPDATE",
#         values=GuildMember.all_columns(),
#         target=GuildMember.user_id,
#     )
#     log.info(f"Inserted {character_name} into db")
#     return character_name


class UpdateUsers:
    @tasks.loop(hours=1)
    async def update_users(self):
        log.info("Updating users")
        guild_members = await GuildMember.objects().prefetch(GuildMember.discord_token)
        for member in guild_members:
            try:
                discord_token: DiscordToken = member.discord_token
                if not discord_token or not discord_token.refresh_token:
                    log.warning(f"Missing Discord token for {member.user_id}")
                    continue
                refreshed_token = await client._http.refresh_oauth2_token(
                    discord_token.refresh_token
                )
                token = OAuth2Token(client, refreshed_token)

                await DiscordToken.update(
                    {
                        DiscordToken.access_token: token.access_token,
                        DiscordToken.refresh_token: token.refresh_token,
                        DiscordToken.expires_at: int(token.expires_at.timestamp()),
                    }
                ).where(DiscordToken.user_id == member.user_id).run()
            except Exception as e:
                log.warning(f"Error refreshing token for {member.user_id}: {e}")
                continue

            # user = await client.fetch_user(token)
            # if not user:
            #     log.error(f"Failed to fetch user with token\n{token}")
            #     continue

            # try:
            #     log.debug(f"Fetching character {name}")
            #     player_character = await PlayerCharacter().create(name)
            # except CharacterNotFound as e:
            #     log.error(f"Error fetching character {name}: {e}")
            #     continue

            # role = RoleConnection(
            #     platform_name=player_character.full_class_name, platform_username=name
            # )
            # role.add_metadata(key="ilvl", value=int(member["ilvl"]))
            # role.add_metadata(key="mplusscore", value=int(float(member["score"])))
            # if member["guild_lb_position"]:
            #     role.add_metadata(key="guildlbposition", value=member["guild_lb_position"])
            # if member["guild_rank"] != "None" and int(member["guild_rank"]) <= 3:
            #     role.add_metadata(key="raider", value=True)

            # changes = await self.update_member_data(member, player_character, role, user)
            # if not changes:
            #     continue

            # try:
            #     await user.edit_role_connection(role)
            #     log.debug(f"Updated user {name}")
            # except (ValueError, TypeError):
            #     log.error(f"Error updating user {name}", exc_info=True)


#     @staticmethod
#     async def update_member_data(member, player_character, role, user):
#         changes = False

#         if player_character.name != member["character_name"]:
#             log.info(f"Updating {player_character.name}'s name")
#             await GuildMember.update(character_name=player_character.name).where(
#                 GuildMember.user_id == str(user.id)
#             ).run()
#             changes = True

#         if player_character.ilvl != int(member["ilvl"]):
#             log.info(f"Updating {player_character.name} ilvl")
#             await GuildMember.update(ilvl=str(player_character.ilvl)).where(
#                 GuildMember.user_id == str(user.id)
#             ).run()
#             role.add_or_edit_metadata(key="ilvl", value=int(player_character.ilvl))
#             changes = True

#         if player_character.score != float(member["score"]):
#             log.info(f"Updating {player_character.name} score")
#             await GuildMember.update(score=str(player_character.score)).where(
#                 GuildMember.user_id == str(user.id)
#             ).run()
#             role.add_or_edit_metadata(key="mplusscore", value=int(player_character.score))
#             changes = True

#         if player_character.guild_lb_position != member["guild_lb_position"]:
#             log.info(f"Updating {player_character.name} guild_lb_position")
#             await GuildMember.update(guild_lb_position=player_character.guild_lb_position).where(
#                 GuildMember.user_id == str(user.id)
#             ).run()
#             if player_character.guild_lb_position:
#                 role.add_or_edit_metadata(
#                     key="guildlbposition", value=player_character.guild_lb_position
#                 )
#             else:
#                 role.remove_metadata(key="guildlbposition")
#             changes = True

#         # Pro tip: Don't ever make everything in a table be Text type :)
#         if player_character.guild_rank is not None and player_character.guild_rank != int(
#             member["guild_rank"]
#         ):
#             # This will need to be changed if we're doing anything other than Raider rank
#             log.info(f"Updating {player_character.name} guild_rank")
#             await GuildMember.update(guild_rank=str(player_character.guild_rank)).where(
#                 GuildMember.user_id == str(user.id)
#             ).run()
#             if player_character.guild_rank is not None and player_character.guild_rank <= 3:
#                 role.add_or_edit_metadata(key="raider", value=True)
#             else:
#                 role.remove_metadata(key="raider")
#             changes = True

#         return changes

#     @update_users.error
#     async def update_users_error(self, error):
#         log.error(f"Unhandled error in update_users: {error}", exc_info=True)
