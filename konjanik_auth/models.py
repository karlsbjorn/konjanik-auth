from piccolo.columns import BigInt, ForeignKey, SmallInt, Text, Varchar
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


class Character(Table):
    character_id = BigInt(primary_key=True, auto_increment=True)
    character_name = Varchar(length=100)
    realm = Varchar(length=100)
    guild = Varchar(length=100, null=True)
    bnet_token = ForeignKey(references=BnetToken)
    ilvl = Text(null=True)
    score = Text(null=True)


class GuildMember(Table):
    user_id = BigInt(primary_key=True, unique=True)
    discord_token = ForeignKey(references=DiscordToken)
    bnet_token = ForeignKey(references=BnetToken)
    guild_rank = Text(null=True)
    guild_lb_position = SmallInt(null=True)
    main_character = ForeignKey(references=Character, null=True)
