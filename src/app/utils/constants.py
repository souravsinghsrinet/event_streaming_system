import os

# DB config
DB_URL = os.environ.get("DB_URL")

# Kafka config
KAFKA_BROKER = os.environ.get("KAFKA_BROKER")

# Redis config
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
CACHE_EXPIRY = 60  # Cache expiry in seconds

# Store active WebSocket connections
ACTIVE_CONNECTIONS = set()
