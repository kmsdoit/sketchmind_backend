import os
from dataclasses import dataclass, asdict
from os import path, environ
from dotenv import load_dotenv



base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
load_dotenv(os.path.join(base_dir,".env"))


@dataclass
class Config:
    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    RROJ_RELOAD: bool = True
    DB_URL: str = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"


@dataclass
class ProdConfig(Config):
    PROJ_RELOADL: bool = True


def conf():
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))
