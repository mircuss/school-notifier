import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = os.environ.get("ADMIN_ID", default="")
TOKEN = os.environ.get("TOKEN", default="")
DB_HOST = os.environ.get("DB_HOST", default="test")
DB_PORT = os.environ.get("DB_PORT", default="test")
DB_NAME = os.environ.get("DB_NAME", default="test")
DB_USER = os.environ.get("DB_USER", default="test")
DB_PASS = os.environ.get("DB_PASS", default="test")



