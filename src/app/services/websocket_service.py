import json

# Store active WebSocket connections
active_connections = set()


# Function to notify WebSocket clients when a new event is added
async def notify_clients(event_data):
    if active_connections:
        message = json.dumps(event_data)
        for connection in active_connections:
            await connection.send_text(message)

