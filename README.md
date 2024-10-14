# data-warehouse

## Data Scraping and Transformation Pipeline

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)

## Introduction
This project focuses on building a robust data scraping and transformation pipeline. The pipeline extracts data from public Telegram channels related to Ethiopian medical businesses, cleans and transforms this data, and implements monitoring and logging systems to ensure data quality. 

## Project Structure
The repository is structured as follows:
``` bash
├── data
│   ├── raw_data.csv          # Raw data scraped from Telegram
│   ├── images/               # Folder storing images scraped
│   ├── last_processed_ids.json  # Tracks the last processed message IDs for each channel
│   └── scraping.log          # Log file for tracking the scraping process
├── scripts
│   ├── telegram_scraper.py   # Script for scraping data from Telegram
│   ├── data_cleaner.py       # Script for cleaning and transforming scraped data
├── README.md                 # Project README file
└── pipeline.log              # Log file for data cleaning and transformation process

```


## Setup and Installation
### Prerequisites
To set up and run the project, ensure you have the following installed:
- Python 3.8 or above
- telethon library for Telegram scraping
- pandas for data cleaning
- dbt (Data Build Tool) for data transformations
### Installation Steps
Clone the repository:
``` bash
git clone https://github.com/your-username/telegram-data-pipeline.git
cd telegram-data-pipeline
```
### To install the required packages, use:
```bash
pip install -r requirements.txt
```
Set up your environment variables in a .env file:
``` bash
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
SCRAPING_LIMIT=100  # Specify the limit for messages to scrape
```
Install and initialize DBT (Data Build Tool) for data transformation:
``` bash
pip install dbt
dbt init my_project
```
## Usage
### Data Scraping
To scrape data from Telegram channels, run the telegram_scraper.py script. This script scrapes text and images from the specified channels and stores the data in CSV and image folders.

``` bash
python scripts/telegram_scraper.py
```
### Data Cleaning and Transformation
After scraping, clean and transform the data by running the data_cleaner.py script. This will remove duplicates, handle missing values, and validate data formats.

``` bash
python scripts/data_cleaner.py
```

### Monitoring and Logging
Logs for both the scraping and cleaning processes can be found in the scraping.log and pipeline.log files in the /data folder. These logs will help you monitor progress and debug any issues.

