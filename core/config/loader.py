from pydantic import Field
from pydantic_settings import BaseSettings


class ConfigEnvs(BaseSettings):
    bot_owner: int = Field(..., alias="BOT_OWNER")
    bot_token: str = Field(..., alias="BOT_TOKEN")

    tira_api_key: str = Field(..., alias="TIRA_API_KEY")

    open_api_key: str = Field(..., alias="OPENAI_API_KEY")

    postgres_name: str = Field(..., alias="POSTGRES_DB")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_pass: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(..., alias="POSTGRES_HOST")
    postgres_port: int = Field(..., alias="POSTGRES_PORT")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    class Config:
        env_file = f".env.dev"
        env_file_encoding = "utf-8"
        extra = "allow"

    @property
    def postgres_url(self) -> str:
        return "postgresql+asyncpg://{postgres_user}:{postgres_pass}@{postgres_host}:{postgres_port}/{postgres_name}".format(
            postgres_user=self.postgres_user,
            postgres_pass=self.postgres_pass,
            postgres_host=self.postgres_host,
            postgres_port=self.postgres_port,
            postgres_name=self.postgres_name,
        )


envs: ConfigEnvs = ConfigEnvs()
