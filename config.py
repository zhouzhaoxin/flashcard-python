from dataclasses import dataclass

from omegaconf import OmegaConf

REMEMBER = {}


@dataclass
class Database:
    SCHEMA: str = "mysql://flashcard:flashcard@127.0.0.1/flashcard"


@dataclass
class Config:
    DATABASE: Database = Database()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


conf = OmegaConf.structured(Config)
