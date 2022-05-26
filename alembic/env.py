from logging.config import fileConfig
import alembic

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sqlalchemy

from alembic import context
from config import TestConfig

alembic_db_config = TestConfig()
print(alembic_db_config)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

db_uri = sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=alembic_db_config.MARIADB_USER,  # e.g. "my-database-user"
            password=alembic_db_config.MARIADB_PASSWORD,  # e.g. "my-database-password"
            host=alembic_db_config.MARIADB_HOST,  # e.g. "127.0.0.1"
            port=alembic_db_config.MARIADB_PORT,  # e.g. 3306
            database=alembic_db_config.DATABASE_NAME,  # e.g. "my-database-name"
            # query={
            #     "driver": "ODBC Driver 17 for SQL Server",  # make sure install mssql in local/docker
            # },
    )


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        url = db_uri
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
        # change sqlalchemy.url
    db_config = config.get_section(config.config_ini_section)
    db_config["sqlalchemy.url"] = db_uri
    
    connectable = engine_from_config(
        # config.get_section(config.config_ini_section),
        db_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
