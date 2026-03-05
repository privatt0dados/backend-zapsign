import os
from dotenv import load_dotenv

load_dotenv()

CLICKSIGN_API_TOKEN = os.getenv("CLICKSIGN_API_TOKEN")
CLICKSIGN_API_URL = os.getenv("CLICKSIGN_API_URL")

EMAIL_EMPRESA = os.getenv("EMAIL_EMPRESA")
NOME_EMPRESA = os.getenv("NOME_EMPRESA")

BASE_URL = os.getenv("BASE_URL")