import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(Path(__file__).resolve().with_name(".env"))

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = BASE_DIR / "attendance.db"
DEFAULT_SQLITE_URL = f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return f"postgresql://{database_url.removeprefix('postgres://')}"
    return database_url


SQLALCHEMY_DATABASE_URL = normalize_database_url(
    os.getenv("SUPABASE_DATABASE_URL")
    or os.getenv("DATABASE_URL")
    or DEFAULT_SQLITE_URL
)


def is_supabase_host(host: str | None) -> bool:
    return bool(host and (host.endswith(".supabase.co") or host.endswith(".pooler.supabase.com")))


def build_engine(database_url: str):
    database_url = normalize_database_url(database_url)
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})

    connect_args = {}
    parsed_url = make_url(database_url)
    if parsed_url.get_backend_name().startswith("postgresql"):
        connect_args["connect_timeout"] = int(os.getenv("DATABASE_CONNECT_TIMEOUT", "3"))
        sslmode = os.getenv("DATABASE_SSLMODE", "").strip()
        if not sslmode and is_supabase_host(parsed_url.host):
            sslmode = "require"
        if sslmode and "sslmode" not in parsed_url.query:
            connect_args["sslmode"] = sslmode

    return create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


def should_fallback_to_sqlite(database_url: str) -> bool:
    if not DEFAULT_SQLITE_PATH.exists():
        return False

    try:
        parsed_url = make_url(database_url)
    except Exception:
        return False

    return parsed_url.get_backend_name().startswith("postgresql") and parsed_url.host in {
        None,
        "localhost",
        "127.0.0.1",
        "::1",
    }


def resolve_engine():
    engine = build_engine(SQLALCHEMY_DATABASE_URL)

    if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        return engine

    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return engine
    except (ModuleNotFoundError, OperationalError, SQLAlchemyError, OSError) as exc:
        if not should_fallback_to_sqlite(SQLALCHEMY_DATABASE_URL):
            raise

        fallback_engine = build_engine(DEFAULT_SQLITE_URL)
        print(
            "Warning: Could not connect to the configured database. "
            f"Falling back to SQLite at {DEFAULT_SQLITE_PATH}. Error: {exc}"
        )
        return fallback_engine


engine = resolve_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
