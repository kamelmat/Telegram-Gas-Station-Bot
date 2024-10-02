
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
