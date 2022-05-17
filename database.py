import pyodbc
import sqlalchemy
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# todo: async connection comes here
# not working with mmsql
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import AsyncSession

db_host = config("db", default="localhost", cast=str)
db_port = config("3306", default=3305, cast=int)
db_user = config("root", default="root")
db_pass = config("MARIADB_ROOT_PASSWORD", default="example")
db_name = config("travel_db", default="travel_db")

db_uri = sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        host=db_host,  # e.g. "127.0.0.1"
        port=db_port,  # e.g. 3306
        database=db_name,  # e.g. "my-database-name"
        # query={
        #     "driver": "ODBC Driver 17 for SQL Server",  # make sure install mssql in local/docker
        # },
    )
    
    
engine = create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    db_uri,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)

Base = declarative_base()
