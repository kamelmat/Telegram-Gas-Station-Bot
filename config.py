import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

TOKEN = os.getenv('TOKEN')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
# FUEL_API_KEY = os.getenv('FUEL_API_KEY')  # Remove this line

# Debugging prints


