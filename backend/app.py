from flask import Flask, jsonify, render_template
from flask_cors import CORS  
import asyncio
import websockets
from collections import deque
from statistics import mean, variance
import json 

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  

# Store the last 20 temperature data points in a deque (FIFO)
data_window = deque(maxlen=20)
all_temperature_data = []  # List to store all temperature data points
latest_data = {"temperature": None, "mean": None, "variance": None, "anomaly": None, "predicted" : None}

async def fetch_data_from_ws():
    """Connect to WebSocket server and fetch temperature data."""
    async with websockets.connect("ws://localhost:8080") as websocket:
        print("Connected to WebSocket server...")
        while True:
            message = await websocket.recv()
            process_weather_data(message)

def process_weather_data(raw_data):
    """Process the incoming weather data, detect anomalies, and update the latest data."""
    global latest_data

    try:
        data = json.loads(raw_data)  # Parse JSON data from WebSocket
        temperature = float(data["Temperature"])  # Extract the temperature value

        # Add the new temperature to the data window and all temperature data
        data_window.append(temperature)

        # Calculate mean, variance, and detect anomaly if we have sufficient data points
        if len(data_window) >= 20:
            current_mean = mean(data_window)
            current_variance = variance(data_window)
            # Anomaly detection: Check if temperature lies outside (mean ± 3 * std_dev)
            anomaly = abs(temperature - current_mean) > 2*(current_variance ** 0.5)
            if (anomaly and data["noise"] == True) or (not anomaly and data["noise"] == False):
                predicted =  True
            else:
                predicted = False
        else:
            current_mean = temperature
            current_variance = 0.0
            anomaly = False
            predicted = True

        # Update the latest data for frontend consumption
        latest_data = {
            "temperature": round(temperature, 2),
            "mean": round(current_mean, 2),
            "variance": round(current_variance, 2),
            "anomaly": anomaly,
            "predicted": predicted
        }

        # Append the latest data to all_temperature_data
        all_temperature_data.append({
            "temperature": latest_data["temperature"],
            "mean": latest_data["mean"],
            "variance": latest_data["variance"],
            "anomaly": latest_data["anomaly"],
            "predicted": latest_data["predicted"]
        })

    except (KeyError, ValueError) as e:
        print(f"Error processing data: {e}")

@app.route('/weather-data')
def get_weather_data():
    """Serve the latest processed weather data to the frontend."""
    return jsonify({
        "latest": latest_data,
        "history": all_temperature_data  # Return all temperature data points
    })

@app.route('/')
def index():
    """Render the frontend template."""
    # return render_template('index.html')

def start_ws_loop():
    """Start the event loop to fetch data from the WebSocket server."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_data_from_ws())

if __name__ == "__main__":
    # Start the WebSocket fetching loop in a background thread
    import threading
    ws_thread = threading.Thread(target=start_ws_loop)
    ws_thread.start()

    # Run the Flask server on localhost with debug mode for auto-reloading
    app.run(port=5000, debug=True)
