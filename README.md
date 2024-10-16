# Live Data Ticker and Anamoly Detection

## Setting up docker and installing required libraries

First make the docker daemon active on the device then by running the following commands
a redis container will run inside the machine

```
docker run -d -p 6379:6379 --name <container_name> redis
pip install -r requirements.txt
```

## Starting the real time data sending service

In case of real world this data is usually found from an aggregator, in case of stocks it 
is Broker and in case of weather api's provided by companies such as OpenWeatherMap

```
python publish.py
```

## Starting the backend services 

To fetch data from the redis channel and a websocket server to broadcast the messages

```
python backend/main.py
```

To start the backend application that would do the calculations and fetch data. This 
will communicate to the backend server created above. Like real world stock data this 
data is also stored in memory and not in a database, it can be easily pushed to a database.
The data is usually stored in memory so that there is low latency

```
python backend/app.py
```

## Starting the frontend

The frontend was created using React and styled using Tailwind. It was created to show the results 
and can be decorated fancily if required. 

The page will show the fetched data and render it on the screen, it can either show the complete data or the last 10 datapoints in reverse order

A green colour indicates that our prediction of whether it is an anomaly or not is correct. 

```
cd frontend
npm install
npm run dev
```

## Things to add

The backend is being polled and the calculations are being done on one backend and the server is sending data from one, these can be merged together which would reduce the cost of calling the server so many times.
A singleton can be created to handle multiple users who are listening to multiple stocks, it is already present in one of the other repository, that can handle state manangements at the backend more efficiently





