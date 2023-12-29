from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int

@dataclass
class DatabaseUrls:
    async_db_url: str


@dataclass
class Settings:
    bots: Bots
    db_urls: DatabaseUrls


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN_API'),
            admin_id=env.int('ADMIN_ID')
        ),
        db_urls=DatabaseUrls(
            async_db_url=env.str('DATABASE_URL')
        )
    )


settings = get_settings('.env')
