import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils import find_cheapest_gas_station, get_gas_station_info  # Import the function here

# Set up logging
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bienvenido, Por favor comparte tu ubicación así puedo buscar la estación de servicio más barata cerca tuyo!.')

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.location:
        lat, lon = update.message.location.latitude, update.message.location.longitude
        cheapest_station = find_cheapest_gas_station(lat, lon)
        if cheapest_station:
            price_message = "Price not available"  # Default message

            # Remove the gas price retrieval
            # gas_price = get_gas_price(cheapest_station['latitude'], cheapest_station['longitude'])
            # if gas_price is not None:
            #     price_message = f"${gas_price:.2f}"

            # Create a Google Maps search link using the gas station's name
            station_name = cheapest_station['name'].replace(" ", "+")  # Format the name for the URL
            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={station_name}"

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
