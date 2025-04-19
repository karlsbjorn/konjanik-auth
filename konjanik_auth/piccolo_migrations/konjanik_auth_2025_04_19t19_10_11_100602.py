from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import BigInt, Text
from piccolo.columns.indexes import IndexMethod

ID = "2025-04-19T19:10:11:100602"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="konjanik_auth", description=DESCRIPTION)

    manager.add_table(
        class_name="DiscordToken",
        tablename="discord_token",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="user_id",
        db_column_name="user_id",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": None,
            "null": True,
            "primary_key": True,
            "unique": True,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="access_token",
        db_column_name="access_token",
        column_class_name="Text",
        column_class=Text,
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
        schema=None,
    )

    manager.add_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="refresh_token",
        db_column_name="refresh_token",
        column_class_name="Text",
        column_class=Text,
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
        schema=None,
    )

    manager.add_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="expires_at",
        db_column_name="expires_at",
        column_class_name="BigInt",
        column_class=BigInt,
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
        schema=None,
    )

    return manager
