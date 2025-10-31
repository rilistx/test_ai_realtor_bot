from alembic import context

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy import engine_from_config

from core.db.model import BaseModel
from core.config.loader import envs


config = context.config


if config.config_file_name is not None:
    fileConfig(
        fname=config.config_file_name,
    )

config.set_main_option(
    name="sqlalchemy.url",
    value=envs.postgres_url + "?async_fallback=True",
)

target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option(
        name="sqlalchemy.url",
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(
            name=config.config_ini_section,
            default={},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
