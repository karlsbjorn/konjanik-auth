from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from konjanik_auth import config

DB = PostgresEngine(config=config.DB_CONFIG)


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["konjanik_auth.piccolo_app"])
