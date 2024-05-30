# # config.py
# import logging
# from pydantic import BaseSettings
#
# logger = logging.getLogger(__name__)
#
# class Settings(BaseSettings):
#     db_url: str
#
#     class Config:
#         env_file = ".env"
#
# def get_settings() -> Settings:
#     settings = Settings()
#     logger.debug("Loaded settings: %s", settings)
#     return settings()
#
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
