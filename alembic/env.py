# this Alembic's runtime script. we've customized it to:
# 1 read the database URL from our .env (not alembic.ini)
# 2. Import our SQLModel classes so autogenerate can see them

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.config import settings
from app.database import engine
from sqlmodel import SQLModel
# this let's you import every model so SQLModel.metadata knows about them
# Add new models here whenever we create them.
from app.models import role  # noqa: F401
from app.models import role, user, driver,vehicle,vehicle_assignment,trip,audit_log
# alembic's own config object; we override the URL below.
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Standard Alembic logging setup.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# What alembic compares against to detect schema changes.
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()