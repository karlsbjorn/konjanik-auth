from piccolo.columns import BigInt, SmallInt, Text, Varchar
from piccolo.table import Table


class GuildMember(Table):
    user_id = BigInt(null=True, default=None, unique=True)
    character_name = Text(null=True, default=None, unique=True)
    guild_rank = Text(null=True, default=None)
    ilvl = Text(null=True, default=None)
    score = Text(null=True, default=None)
    guild_lb_position = SmallInt(null=True, default=None)
    access_token = Text(null=True, default=None)
    refresh_token = Text(null=True, default=None)
    token_expires_at = Text(null=True, default=None)


class AssignedCharacter(Table):
    user_id = BigInt(primary_key=True, null=True, default=None, unique=True)
    character_name = Varchar(null=True, default=None, unique=True)


class DiscordToken(Table):
    user_id = BigInt(primary_key=True, null=True, default=None, unique=True)
    access_token = Text(null=True, default=None)
    refresh_token = Text(null=True, default=None)
    expires_at = BigInt(null=True, default=None)


class BnetToken(Table):
    user_id = BigInt(primary_key=True, null=True, default=None, unique=True)
    access_token = Text(null=True, default=None)
    token_type = Varchar(length=50, null=True, default=None)
    expires_at = BigInt(null=True, default=None)
    scope = Text(null=True, default=None)
    sub = Text(null=True, default=None)  # bnet id
