import os

from dotenv import load_dotenv

load_dotenv()

# Here we will get our weather API KEY which is present in our .env
WEATHER_API_KEY = os.getenv("API_KEY", "")
