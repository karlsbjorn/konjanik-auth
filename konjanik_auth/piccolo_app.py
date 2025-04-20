import os

from piccolo.conf.apps import AppConfig

from .models import BnetToken, Character, DiscordToken, GuildMember

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

APP_CONFIG = AppConfig(
    app_name="konjanik_auth",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=[GuildMember, Character, BnetToken, DiscordToken],
    migration_dependencies=[],
    commands=[],
)
