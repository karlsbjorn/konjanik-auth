import asyncio

import config
from linked_roles import LinkedRolesOAuth2, RoleMetadataRecord


async def main():
    client = LinkedRolesOAuth2(client_id=config.DISCORD_CLIENT_ID, token=config.DISCORD_TOKEN)
    async with client:
        records = (
            RoleMetadataRecord(
                key="ilvl",
                name="Item Level",
                type=2,
                description="Item level korisnika",
            ),
            RoleMetadataRecord(
                key="mplusscore",
                name="M+ Score",
                type=2,
                description="M+ Score korisnika",
            ),
            RoleMetadataRecord(
                key="guildlbposition",
                name="Pozicija na ljestvici",
                type=1,
                description="Pozicija korisnika na ljestvici",
            ),
            # RoleMetadataRecord(
            #     key="guild_master",
            #     name="Guild Master",
            #     type=7,
            #     description="Korisnik je rank Guild Master",
            # ),
            # RoleMetadataRecord(
            #     key="officer",
            #     name="Officer",
            #     type=7,
            #     description="Korisnik je rank Officer",
            # ),
            RoleMetadataRecord(
                key="raider",
                name="Raider",
                type=7,
                description="Korisnik je rank Raider ili iznad",
            ),
            # RoleMetadataRecord(
            #     key="member",
            #     name="Member",
            #     type=7,
            #     description="Korisnik je rank Member",
            # ),
            # RoleMetadataRecord(
            #     key="trial",
            #     name="Trial",
            #     type=7,
            #     description="Korisnik je rank Trial",
            # ),
            # RoleMetadataRecord(
            #     key="social",
            #     name="Social",
            #     type=7,
            #     description="Korisnik je rank Social",
            # ),
        )

        records = await client.register_role_metadata(records=records, force=True)

        print(records)


if __name__ == "__main__":
    asyncio.run(main())
