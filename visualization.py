import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

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

def find_common_user_id():
    heart_rate_query = """
    SELECT DISTINCT Id
    FROM heart_rate;
    """
    sleep_query = """
    SELECT DISTINCT Id
    FROM sleep;
    """
    heart_rate_users = pd.read_sql(heart_rate_query, db_connection)
    sleep_users = pd.read_sql(sleep_query, db_connection)

    common_user_ids = set(heart_rate_users['Id']).intersection(set(sleep_users['Id']))
    if common_user_ids:
        return list(common_user_ids)[0]
    else:
        print("No common user IDs found in both datasets.")
        return None

def extract_data(user_id):
    heart_rate_query = f"""
    SELECT
        Id,
        DATE(Time) AS Day,
        AVG(Value) AS AvgHeartRate,
        MIN(Value) AS MinHeartRate,
        MAX(Value) AS MaxHeartRate,
        STDDEV(Value) AS StdDevHeartRate
    FROM heart_rate
    WHERE Id = {user_id}
    GROUP BY Id, Day
    ORDER BY Id, Day;
    """
    heart_rate_df = pd.read_sql(heart_rate_query, db_connection)
    heart_rate_df['Day'] = pd.to_datetime(heart_rate_df['Day'])

    sleep_query = f"""
    SELECT *
    FROM sleep
    WHERE Id = {user_id};
    """
    sleep_df = pd.read_sql(sleep_query, db_connection)
    sleep_df['date'] = pd.to_datetime(sleep_df['date'])

    # Aggregate sleep data by day
    sleep_df['Day'] = sleep_df['date'].dt.date
    sleep_df['Day'] = pd.to_datetime(sleep_df['Day'])
    sleep_agg_df = sleep_df.groupby('Day').agg({
        'value': 'mean'  # Here we use mean, but you can use other aggregations like sum or max based on your needs
    }).reset_index()

    # Debugging: Print date ranges and data
    print(f"Heart Rate Data Range: {heart_rate_df['Day'].min()} to {heart_rate_df['Day'].max()}")
    print(f"Sleep Data Range: {sleep_df['date'].min()} to {sleep_df['date'].max()}")

    merged_df = pd.merge(heart_rate_df, sleep_agg_df, on='Day', how='inner')

    # Debugging: Print data
    print("Extracted heart rate data:")
    print(heart_rate_df.head())
    print("Aggregated sleep data:")
    print(sleep_agg_df.head())
    print("Merged data:")
    print(merged_df.head())
    
    return merged_df

if __name__ == "__main__":
    user_id = find_common_user_id()
    if user_id:
        print(f"Using common user ID: {user_id}")
        merged_df = extract_data(user_id)
        print(merged_df.head())
    else:
        print("No common user ID found. Please ensure data exists for a user in both datasets.")


