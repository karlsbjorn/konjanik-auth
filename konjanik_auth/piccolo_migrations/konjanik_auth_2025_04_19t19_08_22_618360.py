from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import BigInt, Text

ID = "2025-04-19T19:08:22:618360"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="konjanik_auth", description=DESCRIPTION)

    manager.alter_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="user_id",
        db_column_name="user_id",
        params={},
        old_params={},
        column_class=BigInt,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="user_id",
        db_column_name="user_id",
        params={},
        old_params={},
        column_class=BigInt,
        old_column_class=Text,
        schema=None,
    )

    return manager
