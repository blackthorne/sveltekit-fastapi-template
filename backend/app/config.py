"""Application settings loaded from environment / .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Generate a real secret with: python -c "import secrets; print(secrets.token_hex(32))"
    secret_key: str = "CHANGE_ME_dev_only_secret_padded_to_32_bytes_minimum"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24h; shorten in production

    # Comma-separated list of allowed CORS origins.
    # The tauri:// / http://tauri.localhost origins are what the packaged
    # desktop app uses (macOS+Linux vs Windows respectively).
    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:3000,"
        "tauri://localhost,"
        "http://tauri.localhost"
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
