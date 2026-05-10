import os
from sqlalchemy import create_engine

raw_url = os.getenv("DATABASE_URL")

# This small fix adds '+pymysql' automatically if it's missing
if raw_url and raw_url.startswith("mysql://"):
    DATABASE_URL = raw_url.replace("mysql://", "mysql+pymysql://", 1)
else:
    DATABASE_URL = raw_url

engine = create_engine(DATABASE_URL)
