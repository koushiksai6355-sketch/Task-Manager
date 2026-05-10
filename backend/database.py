import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Get the URL
raw_url = os.getenv("DATABASE_URL")

if not raw_url:
    raise ValueError("DATABASE_URL is missing!")

# 2. Fix the driver prefix
if raw_url.startswith("mysql://"):
    DATABASE_URL = raw_url.replace("mysql://", "mysql+pymysql://", 1)
else:
    DATABASE_URL = raw_url

# 3. Create the Engine
engine = create_engine(DATABASE_URL)

# 4. Create the Session (This was missing!)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create the Base class (This was missing!)
Base = declarative_base()
