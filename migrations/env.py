import os
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio
from app.db.db_config import DATABASE_URL

# os.environ["DATABASE_URL"] = DATABASE_URL

# Import your models' Base
from app.models.inventory import Base

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Get DB URL from environment variable (fallback to alembic.ini)
# DATABASE_URL = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))


# def run_migrations_online():
#     connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

#     async def do_run_migrations():
#         async with connectable.connect() as connection:
#             await connection.run_sync(do_migrations)

#     def do_migrations(connection):
#         context.configure(connection=connection, target_metadata=target_metadata)
#         with context.begin_transaction():
#             context.run_migrations()

#     asyncio.run(do_run_migrations())


# if context.is_offline_mode():
#     # Optional: implement offline migrations if needed
#     pass
# else:
#     run_migrations_online()


if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)


connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)


async def run_migrations_online():
    async with connectable.connect() as connection:
        await connection.run_sync(do_migrations)


def do_migrations(connection):
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


import asyncio

asyncio.run(run_migrations_online())
