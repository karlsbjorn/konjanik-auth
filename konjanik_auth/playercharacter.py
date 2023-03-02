from raiderio_async import RaiderIO


class PlayerCharacter:
    name: str
    ilvl: int
    score: float
    spec_and_class: str
    guild_rank: int

    @classmethod
    async def create(cls, name: str):
        self = PlayerCharacter()
        self.name = name

        data = await self.get_character_data()

        self.ilvl = data["character"]["items"]["item_level_equipped"]
        self.score = data["keystoneScores"]["allScore"]
        self.guild_rank = data["rank"]

        return self

    async def get_character_data(self):
        async with RaiderIO() as rio:
            # This shouldn't be accessed every time, but the lib uses caching, so it's probably ok
            guild_data = await rio.get_guild_roster("eu", "ragnaros", "Jahaci Rumene Kadulje")
        if data := next(
            (
                character
                for character in guild_data["guildRoster"]["roster"]
                if character["character"]["name"] == self.name
            ),
            None,
        ):
            return data
        else:
            raise CharacterNotFound("Character not found")


class CharacterNotFound(Exception):
    pass
