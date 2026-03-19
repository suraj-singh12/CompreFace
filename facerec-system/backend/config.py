import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
DB_PATH = os.getenv("DB_PATH", "../data/db.json")
THRESHOLD = float(os.getenv("THRESHOLD", 0.75))