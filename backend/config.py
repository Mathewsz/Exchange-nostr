from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Configurações de segurança
    SECRET_KEY: str = Field(default="sua_chave_secreta_aqui", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configurações de Nostr
    NOSTR_RELAYS: list = [
        "wss://relay.damus.io",
        "wss://relay.nostr.band",
        "wss://nostr.wine"
    ]

    # Configurações de Blockchain
    BITCOIN_RPC_HOST: str = "localhost"
    BITCOIN_RPC_PORT: int = 8332
    LIGHTNING_RPC_HOST: str = "localhost"
    LIGHTNING_RPC_PORT: int = 9735

    # Configurações de segurança adicionais
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
