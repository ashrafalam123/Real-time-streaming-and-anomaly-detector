import pandas as pd
import redis
import time
import json

# Redis client setup
client = redis.Redis(host='localhost', port=6379, db=0)

# CSV file path
file_path = 'weather_data.csv'
weather_data = []  # More accurate type

# Load weather data from CSV
def load_weather_data():
    global weather_data
    weather_data = pd.read_csv(file_path).to_dict(orient='records')
    print('CSV file successfully processed')

# Publish weather data to Redis
def start_ticker():
    try:
        print("Starting real-time data transfer")
        while True:
            for record in weather_data:
                client.publish("Weather_data", json.dumps(record))
                # Wait 1 second before publishing the next data
                time.sleep(1)
    except Exception as err:
        print('Error during Redis operation:', err)

# Main function to load data and start ticker
def main():
    try:
        load_weather_data()  # Load CSV data
        print("weatherData loaded")
        # Optionally log all data
        # for data in weather_data:
        #     print(data)
        # Start the ticker to publish data
        start_ticker()
    except Exception as error:
        print('Error in main function:', error)

if __name__ == "__main__":
    main()
