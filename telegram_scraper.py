# telegram_scraper.py

import os
import csv
import json
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
last_id_storage_path = './data/last_processed_ids.json'  # JSON file for last IDs

# Create directories if they don’t exist
os.makedirs(image_storage_path, exist_ok=True)

# Load the last processed IDs from JSON
def load_last_processed_ids():
    if os.path.exists(last_id_storage_path):
        with open(last_id_storage_path, 'r') as f:
            return json.load(f)
    return {}

# Save the last processed IDs to JSON
def save_last_processed_id(channel, last_id):
    last_ids = load_last_processed_ids()
    last_ids[channel] = last_id
    with open(last_id_storage_path, 'w') as f:
        json.dump(last_ids, f)

# Function to save messages to a CSV file
def save_data(data):
    file_exists = os.path.isfile(data_storage_path)

    with open(data_storage_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

# Scraping function for both text and images
async def scrape_telegram():
    last_ids = load_last_processed_ids()

    for channel in text_channels:
        try:
            last_id = last_ids.get(channel, 0)  # Start from the last processed message ID
            entity = await client.get_entity(channel)  # Get channel entity
            
            async for message in client.iter_messages(entity, min_id=last_id, limit=scraping_limit):
                # Prepare message data
                data = {
                    'Channel Title': entity.title,  # Channel title
                    'Channel Username': channel,  # Channel username
                    'ID': message.id,  # Message ID
                    'Message': message.text or '',  # Message content
                    'Date': message.date.isoformat(),  # Message date
                    'Media Path': None  # Media path placeholder
                }
                
                # Check if the channel is designated for image scraping and contains media
                if channel in image_channels and message.media:
                    media_path = await message.download_media(file=image_storage_path)
                    data['Media Path'] = media_path

                # Save the message data and update last processed ID
                save_data(data)
                save_last_processed_id(channel, message.id)  # Save last processed ID
                logging.info(f"Saved message {message.id} from channel {channel}.")

        except Exception as e:
            logging.error(f"Error scraping channel {channel}: {str(e)}")

# Main function to run the script
with client:
    client.loop.run_until_complete(scrape_telegram())
