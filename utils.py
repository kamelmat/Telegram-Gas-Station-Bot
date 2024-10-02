import requests
import logging
from bs4 import BeautifulSoup
from config import GOOGLE_MAPS_API_KEY  # Only import GOOGLE_MAPS_API_KEY

logger = logging.getLogger(__name__)

def get_gas_price_from_website(station_name: str) -> float:
    # Implement logic to find the gas station's website and scrape the price
    # This is a placeholder function
    return 2.99  # Replace with actual scraping logic

def find_cheapest_gas_station(lat: float, lon: float) -> dict:
    # Overpass API query to find gas stations within a 5 km radius
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="fuel"](around:5000,{lat},{lon});
      way["amenity"="fuel"](around:5000,{lat},{lon});
      relation["amenity"="fuel"](around:5000,{lat},{lon});
    );
    out body;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    results = response.json()

    if results['elements']:
        station = results['elements'][0]
        return {
            'name': station.get('tags', {}).get('name', 'Unknown Station'),
            'address': station.get('tags', {}).get('addr:full', 'Address not available'),
            'latitude': station.get('lat', None),  # Ensure latitude is extracted
            'longitude': station.get('lon', None),  # Ensure longitude is extracted
            'price': "Price not available"  # Placeholder for price
        }
    else:
        return None

def get_gas_station_info(station_name: str) -> dict:
    # This is a placeholder for the actual implementation.
    # You can use web scraping or an API to get more details about the gas station.
    
    # Example: Searching for the gas station on a search engine or a specific website
    search_url = f"https://www.google.com/search?q={station_name.replace(' ', '+')}+gas+station+price"
    
    # Perform a GET request to the search URL
    response = requests.get(search_url)
    
    # Use BeautifulSoup to parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract relevant information (this will depend on the structure of the website)
    # This is just an example; you will need to adjust the selectors based on the actual HTML structure.
    website = soup.find('a', href=True)  # Example selector
    phone = "123-456-7890"  # Placeholder, implement actual extraction logic
    additional_info = "Open 24 hours"  # Placeholder, implement actual extraction logic

    return {
        'website': website['href'] if website else 'Not available',
        'phone': phone,
        'additional_info': additional_info
    }

# Remove this function if it exists
def get_gas_price(lat: float, lon: float) -> float:
    # Function implementation
    pass  # Remove this entire function