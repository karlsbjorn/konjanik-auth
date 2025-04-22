from piccolo.columns import BigInt, ForeignKey, SmallInt, Text, Varchar, Integer
from piccolo.table import Table


class DiscordToken(Table):
    user_id = BigInt(primary_key=True, unique=True)
    access_token = Text(null=True)
    refresh_token = Text(null=True)
    expires_at = BigInt(null=True)


class BnetToken(Table):
    user_id = BigInt(primary_key=True, unique=True)
    access_token = Text(null=True)
    token_type = Varchar(length=50, null=True)
    expires_at = BigInt(null=True)
    scope = Text(null=True)
    sub = Text(null=True)  # bnet id


class GuildMember(Table):
    user_id = BigInt(primary_key=True, unique=True)
    discord_token = ForeignKey(references=DiscordToken)
    bnet_token = ForeignKey(references=BnetToken)
    guild_rank = Text(null=True)
    guild_lb_position = SmallInt(null=True)
    main_character_id = Integer(null=True)


class Character(Table):
    character_id = BigInt(primary_key=True, unique=True)
    character_name = Varchar(length=100)
    realm_id = BigInt()
    realm = Varchar(length=100)
    guild = Varchar(length=100, null=True)
    bnet_token = ForeignKey(references=BnetToken)
    ilvl = Text(null=True)
    score = Text(null=True)
    guild_member = ForeignKey(references=GuildMember)
