import torch
import os
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
import logging

# Set up logging
logging.basicConfig(filename='../logs/yolo_detection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class YoloDetectionPipeline:
    def __init__(self, model_name='yolov5s', db_url='postgresql://postgres:password@localhost:5432/cleaned_database'):
        self.model = torch.hub.load('ultralytics/yolov5', model_name)
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        # Adjusting column names to match the database schema
        self.detection_table = Table('object_detection_results', self.metadata,
                                     Column('image_id', String),
                                     Column('x_min', Float),   # Updated
                                     Column('y_min', Float),   # Updated
                                     Column('x_max', Float),   # Updated
                                     Column('y_max', Float),   # Updated
                                     Column('confidence', Float),
                                     Column('label', String))
        self.metadata.create_all(self.engine)

    def process_images(self, image_folder='../data/images', output_folder='../data/detection_results/detection_results'):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for img_name in os.listdir(image_folder):
            img_path = os.path.join(image_folder, img_name)
            try:
                results = self.model(img_path)
                results_df = self.sanitize_and_filter_results(results.pandas().xyxy[0])

                # Save the image with detections
                results.save(save_dir=output_folder)
                print(f"Processed {img_name} with detections:\n{results_df[['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']]}")

                # Insert into database if there are detections
                if not results_df.empty:
                    self.save_results(img_name, results_df)
                else:
                    print(f"No detections for {img_name}, skipping database insert.")

            except Exception as e:
                print(f"Error processing {img_name}: {e}")

    def sanitize_and_filter_results(self, results_df):
        """Ensure bounding box coordinates are non-negative and filter valid detections."""
        # Drop rows with invalid bounding boxes and limit to expected ranges
        valid_df = results_df[(results_df['xmin'] >= 0) & (results_df['ymin'] >= 0) & 
                              (results_df['xmax'] > results_df['xmin']) & 
                              (results_df['ymax'] > results_df['ymin'])]
        return valid_df

    def save_results(self, img_id, results_df):
        media_path = os.path.join('../data/images', img_id)
        try:
            with self.engine.connect() as conn:
                for _, row in results_df.iterrows():
                    # Check if the image_id already exists
                    existing_count = conn.execute(
                        self.detection_table.select().where(self.detection_table.c.image_id == img_id)
                    ).fetchone()

                    if existing_count is None:  # If it doesn't exist
                        conn.execute(self.detection_table.insert().values(
                            image_id=img_id,
                            x_min=row['xmin'],       
                            y_min=row['ymin'],       
                            x_max=row['xmax'],       
                            y_max=row['ymax'],       
                            confidence=row['confidence'],
                            label=row['name']
                        ))
                    else:
                        print(f"Skipping insertion for {img_id} as it already exists in the database.")
        except SQLAlchemyError as e:
            print(f"Error inserting row for image {img_id}: {e}")
