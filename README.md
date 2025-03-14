# Event Streaming System

A real-time event streaming system that tracks and processes user activities (e.g., login, purchase, clicks) using Apache Kafka, PostgreSQL, and Redis.

## Project Overview

This system is designed to handle real-time event processing with the following key features:
- Real-time event tracking and processing
- Asynchronous event handling using Kafka
- Persistent storage in PostgreSQL
- Real-time notifications using Redis Pub/Sub
- RESTful API endpoints for event management
- WebSocket support for live event streaming
- Docker-based deployment

## Tech Stack

| Component                | Technology              |
|--------------------------|-------------------------|
| **Backend Framework**    | FastAPI                 |
| **Event Broker**         | Apache Kafka            |
| **Database**             | PostgreSQL              |
| **Real-time Messaging**  | Redis Pub/Sub           |
| **Containerization**     | Docker + Docker Compose |
| **Development Tools**    | Make                    |

## Services

The system consists of the following services:

1. **Application Service** (FastAPI)
   - Handles HTTP requests
   - Produces events to Kafka
   - Exposes REST API endpoints
   - Provides WebSocket endpoint for real-time event streaming
   - Port: 8000

2. **Kafka**
   - Event broker for message streaming
   - Port: 9092
   - Depends on Zookeeper

3. **Zookeeper**
   - Required for Kafka cluster management
   - Port: 2181

4. **PostgreSQL**
   - Persistent storage for events
   - Port: 5432
   - Database: event_db
   - User: user
   - Password: password

5. **Redis**
   - Real-time notifications via Pub/Sub
   - Port: 6379

## Project Structure

```
├── Dockerfile              # Container definition
├── Makefile               # Build and run commands
├── docker-compose.yml     # Service orchestration
├── requirements.txt       # Python dependencies
├── app.env               # Environment variables
└── src/
    ├── app/
    │   ├── main.py      # Application entry point
    │   ├── models/      # Database models
    │   ├── routes/      # API endpoints
    │   ├── schemas/     # Pydantic models
    │   ├── services/    # Business logic
    │   └── utils/       # Helper functions
    ├── run.py           # Application runner
    └── tests/           # Test suite
```

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Make (optional)

### Running the Application

1. Clone the repository:
```bash
git clone <repository-url>
cd event_streaming_system
```

2. Using Docker Compose (recommended):
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

### Environment Variables

Create an `app.env` file with the following variables:
```
KAFKA_BROKER_URL=kafka:9092
POSTGRES_URL=postgresql://user:password@postgres:5432/event_db
REDIS_URL=redis://redis:6379
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### WebSocket Endpoint

The system provides a WebSocket endpoint for real-time event streaming:

```
ws://localhost:8000/v1/ws/events
```

Features:
- Real-time event notifications
- Automatic connection management
- JSON-formatted event data
- Automatic reconnection handling

Example WebSocket client connection:
```javascript
const ws = new WebSocket('ws://localhost:8000/v1/ws/events');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received event:', data);
};

ws.onclose = () => {
    console.log('WebSocket connection closed');
};
```

The WebSocket endpoint will automatically send events to connected clients whenever:
- A new event is tracked through the `/v1/event` endpoint
- The event is successfully processed by the Kafka consumer
- The event is stored in the database

## Development

### Running Tests
```bash
docker-compose run app pytest
```

### Adding New Features
1. Create new models in `src/app/models/`
2. Define schemas in `src/app/schemas/`
3. Add routes in `src/app/routes/`
4. Implement business logic in `src/app/services/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.



