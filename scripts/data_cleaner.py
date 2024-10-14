# scripts/data_cleaner.py

import pandas as pd
import logging
import os
from typing import Optional

class DataCleaner:
    def __init__(self, raw_data_path: str, cleaned_data_path: str):
        self.raw_data_path = raw_data_path
        self.cleaned_data_path = cleaned_data_path
        
        # Set up logging
        logging.basicConfig(filename='../logs/pipeline.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
    def load_data(self) -> pd.DataFrame:
        """Load raw data from a CSV file."""
        logging.info("Loading raw data...")
        data = pd.read_csv(self.raw_data_path)
        logging.info("Data loaded successfully.")
        return data

    def remove_duplicates(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows based on unique identifiers."""
        logging.info("Removing duplicates...")
        data = data.drop_duplicates(subset=['ID', 'Channel Username'])
        logging.info("Duplicates removed.")
        return data

    def handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values by filling or dropping them."""
        logging.info("Handling missing values...")
        data['Message'].fillna('', inplace=True)  # Fill empty messages with an empty string
        data.dropna(subset=['ID', 'Date'], inplace=True)  # Drop rows with missing IDs or Dates
        logging.info("Missing values handled.")
        return data

    def standardize_formats(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize the formats for text, dates, and other columns."""
        logging.info("Standardizing formats...")
        data['Date'] = pd.to_datetime(data['Date'])
        data['Channel Username'] = data['Channel Username'].str.lower().str.strip()
        logging.info("Formats standardized.")
        return data

    def validate_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate data for required fields and formats."""
        logging.info("Validating data...")
        assert data['ID'].dtype == 'int', "ID should be an integer"
        assert data['Date'].notnull().all(), "Date cannot have null values"
        logging.info("Data validation complete.")
        return data

    def save_cleaned_data(self, data: pd.DataFrame):
        """Save the cleaned data to a CSV file."""
        logging.info("Saving cleaned data...")
        data.to_csv(self.cleaned_data_path, index=False)
        logging.info(f"Cleaned data saved to {self.cleaned_data_path}")

    def clean_data(self):
        """Run the entire cleaning process."""
        data = self.load_data()
        data = self.remove_duplicates(data)
        data = self.handle_missing_values(data)
        data = self.standardize_formats(data)
        data = self.validate_data(data)
        self.save_cleaned_data(data)
        logging.info("Data cleaning process complete.")
