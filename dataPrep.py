import pandas as pd

# Define paths to the data files
data_paths = {
    "daily_activity_1": "data/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv",
    "daily_activity_2": "data/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv",
    "heart_rate_1": "data/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/heartrate_seconds_merged.csv",
    "heart_rate_2": "data/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/heartrate_seconds_merged.csv",
    "sleep_1": "data/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/minuteSleep_merged.csv",
    "sleep_2": "data/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/minuteSleep_merged.csv",
}

# Load the data
print("Loading daily activity data...")
daily_activity_1_df = pd.read_csv(data_paths["daily_activity_1"])
daily_activity_2_df = pd.read_csv(data_paths["daily_activity_2"])

print("Loading heart rate data...")
heart_rate_1_df = pd.read_csv(data_paths["heart_rate_1"])
heart_rate_2_df = pd.read_csv(data_paths["heart_rate_2"])

print("Loading sleep data...")
sleep_1_df = pd.read_csv(data_paths["sleep_1"])
sleep_2_df = pd.read_csv(data_paths["sleep_2"])

print("Concatenating data...")
daily_activity_df = pd.concat([daily_activity_1_df, daily_activity_2_df])
heart_rate_df = pd.concat([heart_rate_1_df, heart_rate_2_df])
sleep_df = pd.concat([sleep_1_df, sleep_2_df])

# print concatenated dataframes
print("Daily Activity Data:")
print(daily_activity_df.head())

print("Heart Rate Data:")
print(heart_rate_df.head())

print("Sleep Data:")
print(sleep_df.head())

# check for missing values in csv files
print("Checking for missing values...")
daily_activity_missing = daily_activity_df.isnull().sum()
heart_rate_missing = heart_rate_df.isnull().sum()
sleep_missing = sleep_df.isnull().sum()

print("Daily Activity Missing Values:")
print(daily_activity_missing)

print("Heart Rate Missing Values:")
print(heart_rate_missing)

print("Sleep Missing Values:")
print(sleep_missing)

print("converting date into datatime format...")
daily_activity_df['ActivityDate'] = pd.to_datetime(daily_activity_df['ActivityDate'])
heart_rate_df['Time'] = pd.to_datetime(heart_rate_df['Time'])
sleep_df['date'] = pd.to_datetime(sleep_df['date'])


# 10% sample size
print("Creating 10% sample size...")
sampled_users = daily_activity_df['Id'].drop_duplicates().sample(frac=0.1, random_state=42)
sampled_daily_activity_df = daily_activity_df[daily_activity_df['Id'].isin(sampled_users)]
sampled_heart_rate_df = heart_rate_df[heart_rate_df['Id'].isin(sampled_users)]
sampled_sleep_df = sleep_df[sleep_df['Id'].isin(sampled_users)]

# shape is the number of rows and columns in the dataframe
print("Shape of sampled daily activity data:")
print(sampled_daily_activity_df.shape)
print("Shape of sampled heart rate data:")
print(sampled_heart_rate_df.shape)
print("Shape of sampled sleep data:")
print(sampled_sleep_df.shape)

# # Print the first few rows of each dataframe to confirm loading
# print("Daily Activity Data 1:")
# print(daily_activity_1_df.head())

# print("Daily Activity Data 2:")
# print(daily_activity_2_df.head())

# print("Heart Rate Data 1:")
# print(heart_rate_1_df.head())

# print("Heart Rate Data 2:")
# print(heart_rate_2_df.head())

# print("Sleep Data 1:")
# print(sleep_1_df.head())

# print("Sleep Data 2:")
# print(sleep_2_df.head())
