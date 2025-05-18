import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GKP_CHAT_ID = int(os.getenv("GKP_CHAT_ID"))