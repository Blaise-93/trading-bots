import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("API_KEY")
LIVE_ACCOUNT_ID = os.getenv('LIVE_ACCOUNT_ID')
PAPER_ACCOUNT_ID = os.getenv('PAPER_ACCOUNT_ID')
BASE_URL = 'https://api.3commas.io/public/api'

BACKEND_URL = os.getenv("BACKEND_URL")

BROKER_URL = os.getenv("BROKER_URL")

DATABASE_URL = os.getenv("DATABASE_URL")