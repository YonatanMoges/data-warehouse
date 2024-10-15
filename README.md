# data-warehouse

## Data Scraping and Transformation Pipeline

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Object detection using YOLO](#object-detection-with-yolo)

## Introduction
This project focuses on building a robust data scraping and transformation pipeline. The pipeline extracts data from public Telegram channels related to Ethiopian medical businesses, cleans and transforms this data, and implements monitoring and logging systems to ensure data quality. 

## Project Structure
The repository is structured as follows:
``` bash
├── data
│   ├── raw_data.csv            # Raw data scraped from Telegram
│   ├── images/                 # Folder storing images scraped
│   ├── last_processed_ids.json  # Tracks the last processed message IDs for each channel
│   └── scraping.log            # Log file for tracking the scraping process
├── logs                        # Log directory for pipeline logs
├── my_project                  # DBT project directory
├── notebook                    # Jupyter notebooks
│   ├── __init__.py
│   ├── data_cleaning.ipynb     # Notebook for data cleaning
│   └── yolo_detection.ipynb     # Notebook for YOLO object detection
├── scripts                     # Directory for Python scripts
│   ├── __init__.py
│   ├── data_cleaner.py         # Script for cleaning and transforming scraped data
│   └── yolo_detection.py        # Script for object detection using YOLO
├── yolov5                      # YOLOv5 cloned repository for object detection
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── README.md                   # Project README file
├── requirements.txt            # Required packages
└── telegram_scraper.py         # Script for scraping data from Telegram

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
git clone https://github.com/YonatanMoges/data-warehouse.git
cd data-warehouse
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

## Object Detection with YOLO
After the data has been scraped and cleaned, you can perform object detection on the images using the YOLO algorithm. To do this, run the yolo_detection.py script, which will process the images and store the detection results in a PostgreSQL database.

``` bash
python scripts/yolo_detection.py
```

### Monitoring and Logging
Logs for both the scraping, cleaning, and detection processes can be found in the scraping.log and other log files in the logs directory. These logs will help you monitor progress and debug any issues.