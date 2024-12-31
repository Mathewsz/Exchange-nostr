from pydantic import BaseSettings

class Settings(BaseSettings):
    # Configurações de segurança
    SECRET_KEY: str = "sua_chave_secreta_aqui"
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

settings = Settings()
