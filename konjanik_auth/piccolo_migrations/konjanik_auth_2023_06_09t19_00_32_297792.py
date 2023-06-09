from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import SmallInt
from piccolo.columns.indexes import IndexMethod


ID = "2023-06-09T19:00:32:297792"
VERSION = "0.114.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="konjanik_auth", description=DESCRIPTION)

    manager.add_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="guild_lb_position",
        db_column_name="guild_lb_position",
        column_class_name="SmallInt",
        column_class=SmallInt,
        params={
            "default": None,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    return manager
