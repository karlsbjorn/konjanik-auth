import config
from piccolo.columns import Text
from piccolo.engine import PostgresEngine
from piccolo.table import Table

DB = PostgresEngine(config=config.DB_CONFIG)


class GuildMember(Table, db=DB):
    user_id = Text(null=True, default=None, unique=True)
    character_name = Text(null=True, default=None, unique=True)
    guild_rank = Text(null=True, default=None)
    ilvl = Text(null=True, default=None)
    score = Text(null=True, default=None)
    access_token = Text(null=True, default=None)
    refresh_token = Text(null=True, default=None)
    token_expires_at = Text(null=True, default=None)
