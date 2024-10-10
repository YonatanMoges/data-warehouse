# telegram_scraper.py

import os
import csv
import logging
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load credentials and settings from .env file
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
scraping_limit = int(os.getenv('SCRAPING_LIMIT'))

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Set up logging
logging.basicConfig(filename='./data/scraping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define channels for text and image scraping
text_channels = [
    'DoctorsET',
    'CheMed123',
    'lobelia4cosmetics',
    'yetenaweg',
    'EAHCI'
]

image_channels = [
    'CheMed123',
    'lobelia4cosmetics'
]

# Define data storage paths
data_storage_path = './data/raw_data.csv'  # Change to CSV file
image_storage_path = './data/images/'  # Folder for images

# Create image directory if it doesn’t exist
os.makedirs(image_storage_path, exist_ok=True)

# Function to save messages to a CSV file
def save_data(data):
    # Check if the CSV file exists to write headers only if it's new
    file_exists = os.path.isfile(data_storage_path)

    with open(data_storage_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        
        # Write header only if the file didn't exist before
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

# Scraping function for both text and images
async def scrape_telegram():
    for channel in text_channels:
        try:
            async for message in client.iter_messages(channel, limit=scraping_limit):
                # Prepare message data
                data = {
                    'Channel Title': channel,  # Changed to 'Channel Title'
                    'Channel Username': channel,  # Added 'Channel Username'
                    'ID': message.id,  # Changed to 'ID'
                    'Message': message.text or '',  # Handle None text, changed to 'Message'
                    'Date': message.date.isoformat(),  # Changed to 'Date'
                    'Media Path': None  # Added 'Media Path'
                }
                
                # Check if the channel is designated for image scraping and contains media
                if channel in image_channels and message.media:
                    media_path = await message.download_media(file=image_storage_path)
                    data['Media Path'] = media_path  # Set 'Media Path' if media exists

                # Save the message data
                save_data(data)
                logging.info(f"Saved message {message.id} from channel {channel}.")

        except Exception as e:
            logging.error(f"Error scraping channel {channel}: {str(e)}")

# Main function to run the script
with client:
    client.loop.run_until_complete(scrape_telegram())
