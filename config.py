from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Configs the parameters to initialize the environment
    user: str
    password: str
    account: str
    class Config:
        env_file = ".env"

settings = Settings()

class Costs(BaseSettings):
    cost: float = 0
    class Config:
        env_file = ".config"

costs = Costs()