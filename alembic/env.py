from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
from src.app.database import Base  # tu Base con todos los modelos
from src.app.settings import get_settings

settings = get_settings()

# ---------------- Alembic Config ----------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------- Metadata ----------------
target_metadata = Base.metadata

# ---------------- Database URL ----------------
# Detecta async driver y reemplaza por driver sync para Alembic
db_url = settings.db.db_url
if "+asyncpg" in db_url:
    SQLALCHEMY_DATABASE_URL = db_url.replace("+asyncpg", "")
elif "+aiosqlite" in db_url:
    SQLALCHEMY_DATABASE_URL = db_url.replace("+aiosqlite", "")
else:
    SQLALCHEMY_DATABASE_URL = db_url  # ya sync

# ---------------- Offline Migrations ----------------
def run_migrations_offline():
    url = SQLALCHEMY_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ---------------- Online Migrations ----------------
def run_migrations_online():
    connectable = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# ---------------- Run migrations ----------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()