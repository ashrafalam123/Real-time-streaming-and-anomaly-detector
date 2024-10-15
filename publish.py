import pandas as pd
import redis
import time
import json

#Connect to the redis, it should ideally be running on a docker container on port 6379
client = redis.Redis(host='localhost', port=6379, db=0)

"""
In the real world the data would be fetched from a channel via a websocket

To simulate a channel a file containing the original weather of cities was taken.
Random noise was added to 5% of the dataset and this data was sent to a redis channel
Since this is a weather data it is both regular as well as seasonal
"""

file_path = 'weather_data.csv'
weather_data = []  

def load_weather_data():
    global weather_data
    weather_data = pd.read_csv(file_path).to_dict(orient='records')
    print('CSV file successfully processed')

"""
To simulate the live tickers of financial markets, a sleep of 1 second is added to simulate how the data 
is actually updated in the stock market
"""
def start_ticker():
    try:
        print("Starting real-time data transfer")
        while True:
            for record in weather_data:
                client.publish("Weather_data", json.dumps(record))
                time.sleep(1)
    except Exception as err:
        print('Error during Redis operation:', err)

#The main function

def main():
    try:
        load_weather_data()  
        print("weatherData loaded")
        start_ticker()
    except Exception as error:
        print('Error in main function:', error)

if __name__ == "__main__":
    main()
