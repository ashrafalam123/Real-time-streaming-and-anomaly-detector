import asyncio
import json
import websockets
from websockets import WebSocketServerProtocol
from redis.asyncio import Redis

# Store active WebSocket connections
connected_clients = set()

"""
Subscribe to the redis channel where the data is being published and start a websocket server on the default port 8080
This would broadcast the fetched data from the channel

This can additonally be checked on Hoppscotch if we create a socket connection to this port, the data gets displayed
"""
REDIS_CHANNEL = "Weather_data"
redis = Redis()  

async def broadcast(message: str):
    """Broadcast a message to all connected WebSocket clients."""
    if connected_clients:  
        print(f"Broadcasting message: {message}")
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def handle_client(websocket: WebSocketServerProtocol):
    """Handle a new client connection."""
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")

    try:
        async for _ in websocket:  
            pass 
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")

async def redis_listener():
    """Subscribe to Redis channel and broadcast messages to clients."""
    pubsub = redis.pubsub()
    await pubsub.subscribe(REDIS_CHANNEL)
    print(f"Subscribed to Redis channel: {REDIS_CHANNEL}")

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            await broadcast(json.dumps(data))

async def main():
    """Main function to start WebSocket server and Redis listener."""
    websocket_server = await websockets.serve(handle_client, "localhost", 8080)
    print("WebSocket server started on ws://localhost:8080")

    # Run Redis listener concurrently with WebSocket server
    await asyncio.gather(websocket_server.wait_closed(), redis_listener())

def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    run()
