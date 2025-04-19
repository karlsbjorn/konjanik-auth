from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import BigInt, SmallInt, Text, Varchar
from piccolo.columns.indexes import IndexMethod

ID = "2025-04-19T18:41:48:154963"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="konjanik_auth", description=DESCRIPTION)

    manager.add_table(class_name="BnetToken", tablename="bnet_token", schema=None, columns=None)

    manager.add_table(
        class_name="AssignedCharacter",
        tablename="assigned_character",
        schema=None,
        columns=None,
    )

    manager.add_table(
        class_name="GuildMember",
        tablename="guild_member",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="user_id",
        db_column_name="user_id",
        column_class_name="Text",
        column_class=Text,
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
        table_class_name="BnetToken",
        tablename="bnet_token",
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
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="token_type",
        db_column_name="token_type",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 50,
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
        table_class_name="BnetToken",
        tablename="bnet_token",
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

    manager.add_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="scope",
        db_column_name="scope",
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
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="sub",
        db_column_name="sub",
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
        table_class_name="AssignedCharacter",
        tablename="assigned_character",
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
        table_class_name="AssignedCharacter",
        tablename="assigned_character",
        column_name="character_name",
        db_column_name="character_name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": None,
            "null": True,
            "primary_key": False,
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
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="user_id",
        db_column_name="user_id",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": None,
            "null": True,
            "primary_key": False,
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
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="character_name",
        db_column_name="character_name",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": None,
            "null": True,
            "primary_key": False,
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
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="guild_rank",
        db_column_name="guild_rank",
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
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="ilvl",
        db_column_name="ilvl",
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
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="score",
        db_column_name="score",
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
        schema=None,
    )

    manager.add_column(
        table_class_name="GuildMember",
        tablename="guild_member",
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
        table_class_name="GuildMember",
        tablename="guild_member",
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
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="token_expires_at",
        db_column_name="token_expires_at",
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

    return manager
