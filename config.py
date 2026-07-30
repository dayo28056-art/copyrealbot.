import os
from dotenv import load_dotenv

load_dotenv()

# Bot token from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Image file name
IMAGE_FILE = "welcome.jpg"

# Bot description
BOT_DESCRIPTION = """🧰 CopyBot | Cleans text spaces, strips link trackers, and counts ad characters instantly. Tap /start!"""
