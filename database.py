from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Database URL from environment variable, default to a local PostgreSQL instance
# Format: postgresql://user:password@host:port/database
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/fastapiserver"
)
print(f"DEBUG: Database URL set to: {SQLALCHEMY_DATABASE_URL}")

# For testing, we can override with SQLite in-memory database
# Set DATABASE_URL="sqlite:///./test.db" for file-based test DB
# or DATABASE_URL="sqlite:///:memory:" for in-memory test DB

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # These args are needed for SQLite
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)