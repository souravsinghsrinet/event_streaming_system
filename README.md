# event_streaming_system
A system that tracks user activities in real-time (e.g., login, purchase, clicks)

## Objectives
* Build a system that tracks user activities in real-time (e.g., login, purchase, clicks).
* Use Kafka to stream events & process them asynchronously.
* Store event data in PostgreSQL and use Redis Pub/Sub for live notifications.
* Implement a real-time dashboard API.

## Tech Stack

| Component                | Technology              |
|--------------------------|-------------------------|
| **Backend Framework**    | FastAPI                 |
| **Event Broker**         | Apache Kafka            |
| **Database**             | PostgreSQL              |
| **Real-time Messaging**  | Redis Pub/Sub           |
| **Task Queue**           | Celery                  |
| **Logging & Monitoring** | Prometheus + Grafana    |
| **Containerization**     | Docker + Docker Compose |
| **Deployment**           | Kubernetes (Optional)   |

## Features & Architecture

1. Event Producer (User Activity Tracking)
    * FastAPI-based microservice that logs user events (e.g., login, purchase).
	* Sends the event data to Kafka topics asynchronously.
2. Event Broker (Kafka)
	* Kafka queues events and ensures reliable message delivery.
3. Event Consumer (Processing Service)
	* Reads messages from Kafka topics.
	* Stores them in PostgreSQL for long-term analysis.
	* Uses Redis Pub/Sub to notify other services in real time.
4. Real-time Dashboard API
	* A FastAPI-based API that fetches recent events from PostgreSQL.
	* Can be extended with WebSockets for live updates.

## Project Folder Structure
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
└── src
    ├── app
    │   ├── main.py
    │   ├── models
    │   ├── routes
    │   │   └── v1
    │   ├── schemas
    │   ├── services
    │   └── utils
    │        └── kafka_helper.py
    ├── run.py
    └── tests



