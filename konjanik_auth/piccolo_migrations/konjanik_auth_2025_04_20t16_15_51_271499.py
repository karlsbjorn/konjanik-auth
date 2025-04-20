from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.column_types import BigInt, ForeignKey, SmallInt, Text, Varchar
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class BnetToken(Table, tablename="bnet_token", schema=None):
    user_id = BigInt(
        default=0,
        null=False,
        primary_key=True,
        unique=True,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


class Character(Table, tablename="character", schema=None):
    character_id = BigInt(
        auto_increment=True,
        default=0,
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


class DiscordToken(Table, tablename="discord_token", schema=None):
    user_id = BigInt(
        default=0,
        null=False,
        primary_key=True,
        unique=True,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


ID = "2025-04-20T16:15:51:271499"
VERSION = "1.24.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="konjanik_auth", description=DESCRIPTION)

    manager.add_table(class_name="Character", tablename="character", schema=None, columns=None)

    manager.drop_table(
        class_name="AssignedCharacter",
        tablename="assigned_character",
        schema=None,
    )

    manager.add_column(
        table_class_name="Character",
        tablename="character",
        column_name="character_id",
        db_column_name="character_id",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "auto_increment": True,
            "default": 0,
            "null": False,
            "primary_key": True,
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
        table_class_name="Character",
        tablename="character",
        column_name="character_name",
        db_column_name="character_name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 100,
            "default": "",
            "null": False,
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
        table_class_name="Character",
        tablename="character",
        column_name="realm",
        db_column_name="realm",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 100,
            "default": "",
            "null": False,
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
        table_class_name="Character",
        tablename="character",
        column_name="guild",
        db_column_name="guild",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 100,
            "default": "",
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
        table_class_name="Character",
        tablename="character",
        column_name="bnet_token",
        db_column_name="bnet_token",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": BnetToken,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
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
        table_class_name="Character",
        tablename="character",
        column_name="ilvl",
        db_column_name="ilvl",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
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
        table_class_name="Character",
        tablename="character",
        column_name="score",
        db_column_name="score",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
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

    manager.drop_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="access_token",
        db_column_name="access_token",
        schema=None,
    )

    manager.drop_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="character_name",
        db_column_name="character_name",
        schema=None,
    )

    manager.drop_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="ilvl",
        db_column_name="ilvl",
        schema=None,
    )

    manager.drop_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="refresh_token",
        db_column_name="refresh_token",
        schema=None,
    )

    manager.drop_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="score",
        db_column_name="score",
        schema=None,
    )

    manager.drop_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="token_expires_at",
        db_column_name="token_expires_at",
        schema=None,
    )

    manager.add_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="bnet_token",
        db_column_name="bnet_token",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": BnetToken,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
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
        column_name="discord_token",
        db_column_name="discord_token",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": DiscordToken,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
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
        column_name="main_character",
        db_column_name="main_character",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Character,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
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

    manager.alter_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="user_id",
        db_column_name="user_id",
        params={"default": 0, "null": False, "primary_key": True},
        old_params={"default": None, "null": True, "primary_key": False},
        column_class=BigInt,
        old_column_class=BigInt,
        schema=None,
    )

    manager.alter_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="guild_rank",
        db_column_name="guild_rank",
        params={"default": ""},
        old_params={"default": None},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="GuildMember",
        tablename="guild_member",
        column_name="guild_lb_position",
        db_column_name="guild_lb_position",
        params={"default": 0},
        old_params={"default": None},
        column_class=SmallInt,
        old_column_class=SmallInt,
        schema=None,
    )

    manager.alter_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="user_id",
        db_column_name="user_id",
        params={"default": 0, "null": False},
        old_params={"default": None, "null": True},
        column_class=BigInt,
        old_column_class=BigInt,
        schema=None,
    )

    manager.alter_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="access_token",
        db_column_name="access_token",
        params={"default": ""},
        old_params={"default": None},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="token_type",
        db_column_name="token_type",
        params={"default": ""},
        old_params={"default": None},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    manager.alter_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="expires_at",
        db_column_name="expires_at",
        params={"default": 0},
        old_params={"default": None},
        column_class=BigInt,
        old_column_class=BigInt,
        schema=None,
    )

    manager.alter_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="scope",
        db_column_name="scope",
        params={"default": ""},
        old_params={"default": None},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="BnetToken",
        tablename="bnet_token",
        column_name="sub",
        db_column_name="sub",
        params={"default": ""},
        old_params={"default": None},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="user_id",
        db_column_name="user_id",
        params={"default": 0, "null": False},
        old_params={"default": None, "null": True},
        column_class=BigInt,
        old_column_class=BigInt,
        schema=None,
    )

    manager.alter_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="access_token",
        db_column_name="access_token",
        params={"default": ""},
        old_params={"default": None},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="refresh_token",
        db_column_name="refresh_token",
        params={"default": ""},
        old_params={"default": None},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="DiscordToken",
        tablename="discord_token",
        column_name="expires_at",
        db_column_name="expires_at",
        params={"default": 0},
        old_params={"default": None},
        column_class=BigInt,
        old_column_class=BigInt,
        schema=None,
    )

    return manager
