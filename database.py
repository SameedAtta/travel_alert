import pyodbc
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_env


app_config = get_env()


# todo: async connection comes here
# not working with mmsql
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import AsyncSession

db_host = app_config.MARIADB_HOST
db_port = app_config.MARIADB_PORT
db_user = app_config.MARIADB_USER
db_pass = app_config.MARIADB_PASSWORD
db_name = app_config.DATABASE_NAME
    
    
engine = create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        host=db_host,  # e.g. "127.0.0.1"
        port=db_port,  # e.g. 3306
        database=db_name,  # e.g. "my-database-name"
        # query={
        #     "driver": "ODBC Driver 17 for SQL Server",  # make sure install mssql in local/docker
        # },
    ),
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)

Base = declarative_base()
