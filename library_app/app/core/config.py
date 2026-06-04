from pydantic_settings import BaseSettings, SettingsConfigDict
USERNAME = "username"
PASSWORD = "password"
ROLE = "role"
USER = "user"
ADMIN = "admin"
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
settings = Settings()