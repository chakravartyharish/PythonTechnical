from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.infrastructure.models.db import Base  # Import your Base model for target_metadata
from app.config import get_settings  # Import your configuration to get DB URL

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = get_settings().db_url
    context.configure(
        url=str(url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = create_async_engine(
        str(get_settings().db_url),
        future=True,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
