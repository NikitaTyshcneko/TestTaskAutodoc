import os
import logging
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('', '.env')
load_dotenv(dotenv_path=env_path)
logging.basicConfig(level=logging.DEBUG)

name = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOSTNAME')
port = os.getenv('PORT')

# Construct the DATABASE_URL
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{name}"

# Log connection parameters
logging.debug(f"Connecting to database with URL: {DATABASE_URL}")

ACCESS_TOKEN_EXPIRE_MINUTES = 60*30
MY_ALGORITHMS = os.getenv('MY_ALGORITHMS')
SECRET = os.getenv('SECRET')