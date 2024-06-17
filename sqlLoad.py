import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB = os.getenv('MYSQL_DB')

# Define the connection string using environment variables
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
db_connection = create_engine(db_connection_str)

# Define paths to the heart rate data files
heart_rate_files = [
    "data/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/heartrate_seconds_merged.csv",
    "data/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/heartrate_seconds_merged.csv"
]

# Load, preprocess, and insert data into MySQL table
for file in heart_rate_files:
    # Load CSV data into a DataFrame
    heart_rate_df = pd.read_csv(file)
    
    # Convert 'Time' column to the correct datetime format
    heart_rate_df['Time'] = pd.to_datetime(heart_rate_df['Time'])
    heart_rate_df['Time'] = heart_rate_df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Insert data into MySQL table
    heart_rate_df.to_sql('heart_rate', con=db_connection, if_exists='append', index=False)

print("Data loaded into MySQL database successfully.")


