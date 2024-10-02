# main.py

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN, GOOGLE_MAPS_API_KEY
from handlers import start, handle_location
from utils import find_cheapest_gas_station

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

# config.py

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

# handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from utils import find_cheapest_gas_station

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Please share your location to find the cheapest gas station nearby.')

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.location:
        lat, lon = update.message.location.latitude, update.message.location.longitude
        cheapest_station = find_cheapest_gas_station(lat, lon)
        if cheapest_station:
            price = cheapest_station['price']
            price_message = f"${price:.2f}" if isinstance(price, (int, float)) else "Price not available"

            # Create a Google Maps link
            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={cheapest_station['latitude']},{cheapest_station['longitude']}"

            # Send the gas station information
            await update.message.reply_text(f"The cheapest gas station nearby is:\n\n"
                                            f"Name: {cheapest_station['name']}\n"
                                            f"Address: {cheapest_station['address']}\n"
                                            f"Price: {price_message}\n"
                                            f"View on Google Maps: {google_maps_link}")

            # Optionally, retrieve additional information about the gas station
            additional_info = get_gas_station_info(cheapest_station['name'])
            await update.message.reply_text(f"Website: {additional_info['website']}\n"
                                             f"Phone: {additional_info['phone']}\n"
                                             f"Info: {additional_info['additional_info']}")
        else:
            await update.message.reply_text("Vaya, lo siento. Parece que no he podido encontrar ninguna estación cerca tuyo 😞")
    else:
        await update.message.reply_text("¿Serías tan amable de compartir tu ubicación? 🙏🏼.")

# utils.py

import requests
from config import GOOGLE_MAPS_API_KEY

def find_cheapest_gas_station(lat: float, lon: float) -> dict:
    # This is a placeholder function. You'll need to implement the actual logic
    # to find gas stations and their prices using Google Maps API or another service.
    # For now, it returns a dummy result.
    return {
        'name': 'Sample Gas Station',
        'address': '123 Main St, Anytown, USA',
        'price': 2.99
    }

# test_bot.py

import unittest
from unittest.mock import patch, MagicMock
from handlers import start, handle_location
from utils import find_cheapest_gas_station

class TestTelegramBot(unittest.TestCase):

    @patch('telegram.Update')
    @patch('telegram.ext.ContextTypes.DEFAULT_TYPE')
    async def test_start(self, mock_context, mock_update):
        mock_update.message.reply_text = MagicMock()
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with('Welcome! Please share your location to find the cheapest gas station nearby.')

    @patch('telegram.Update')
    @patch('telegram.ext.ContextTypes.DEFAULT_TYPE')
    @patch('handlers.find_cheapest_gas_station')
    async def test_handle_location(self, mock_find_cheapest, mock_context, mock_update):
        mock_update.message.location.latitude = 40.7128
        mock_update.message.location.longitude = -74.0060
        mock_update.message.reply_text = MagicMock()

        mock_find_cheapest.return_value = {
            'name': 'Test Gas Station',
            'address': '456 Test St, Testtown, USA',
            'price': 2.50
        }

        await handle_location(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(
            "The cheapest gas station nearby is:\n\n"
            "Name: Test Gas Station\n"
            "Address: 456 Test St, Testtown, USA\n"
            "Price: $2.50"
        )

    def test_find_cheapest_gas_station(self):
        result = find_cheapest_gas_station(40.7128, -74.0060)
        self.assertIsInstance(result, dict)
        self.assertIn('name', result)
        self.assertIn('address', result)
        self.assertIn('price', result)

if __name__ == '__main__':
    unittest.main()
