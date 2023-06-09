import logging
from raiderio_async import RaiderIO

log = logging.getLogger(__name__)


class PlayerCharacter:
    name: str
    ilvl: int
    score: float
    char_class: str
    char_spec: str
    guild_rank: int
    guild_lb_position: int

    @classmethod
    async def create(cls, name: str):
        self = PlayerCharacter()
        self.name = name

        # RaiderIO
        data = await self.get_character_data()
        try:
            self.ilvl = data["character"]["items"]["item_level_equipped"]
            self.score = data["keystoneScores"]["allScore"]
            self.char_class = data["character"]["class"]["name"]
            self.char_spec = data["character"]["spec"]["name"]
            self.guild_rank = data["rank"]
            self.guild_lb_position = await self.get_guild_lb_position()
        except KeyError:
            # Character wasn't in guild
            self.ilvl = data["gear"]["item_level_equipped"]
            self.score = data["mythic_plus_scores"]["all"]
            self.char_class = data["class"]
            self.char_spec = data["active_spec_name"]
            self.guild_rank = None
            self.guild_lb_position = None

        return self

    async def get_character_data(self) -> dict:
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

        # If character is not in guild, try to get it from raider.io
        log.info(f"{self.name} not in guild")
        async with RaiderIO() as rio:
            char_data = await rio.get_character_profile(
                "eu", "ragnaros", self.name, ["gear", "mythic_plus_scores"]
            )
        if char_data:
            return char_data

        raise CharacterNotFound("Character not found")

    async def get_guild_lb_position(self) -> int:
        # Get a dict of characters in the guild with their M+ score
        async with RaiderIO() as rio:
            # This shouldn't be accessed every time, but the lib uses caching, so it's probably ok
            guild_data = await rio.get_guild_roster("eu", "ragnaros", "Jahaci Rumene Kadulje")
        lb = {
            character["character"]["name"]: character["keystoneScores"]["allScore"]
            for character in guild_data["guildRoster"]["roster"]
            if character["keystoneScores"]["allScore"]
        }
        # Sort the list by M+ score
        lb = dict(sorted(lb.items(), key=lambda x: x[1], reverse=True))
        # Get the position of the character in the list
        for i, character in enumerate(lb.items()):
            if character[0] == self.name:
                return i + 1


class CharacterNotFound(Exception):
    pass
