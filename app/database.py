import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.settings.settings import DATABASE_URL

db = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
Base = declarative_base()
print(DATABASE_URL)