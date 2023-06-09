from piccolo.columns import Text, BigInt, Varchar, SmallInt
from piccolo.table import Table


class GuildMember(Table):
    user_id = Text(null=True, default=None, unique=True)
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
