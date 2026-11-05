import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    """Pipeline settings read from environment variables (12-factor config).

    Defaults live only in from_env(), so there is a single source of truth.
    """

    db_password: str = field(repr=False)
    db_user: str
    db_host: str
    db_port: int
    db_name: str
    nbp_base_url: str
    http_timeout: int
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        password = os.environ.get("DB_PASSWORD")
        if not password:
            raise RuntimeError("DB_PASSWORD is not set. Copy .env.example to .env and fill it in.")
        return cls(
            db_password=password,
            db_user=os.environ.get("DB_USER", "postgres"),
            db_host=os.environ.get("DB_HOST", "localhost"),
            db_port=int(os.environ.get("DB_PORT", "5432")),
            db_name=os.environ.get("DB_NAME", "nbp"),
            nbp_base_url=os.environ.get("NBP_BASE_URL", "https://api.nbp.pl/api"),
            http_timeout=int(os.environ.get("HTTP_TIMEOUT", "10")),
            log_level=os.environ.get("LOG_LEVEL", "INFO"),
        )

    @property
    def db_conninfo(self) -> str:
        """psycopg 3 connection string. Contains the password: never log it."""
        return (
            f"host={self.db_host} port={self.db_port} dbname={self.db_name} "
            f"user={self.db_user} password={self.db_password}"
        )
