import pytest
from fastapi.testclient import TestClient
from src.app.models.event_model import Event
from sqlalchemy.orm import Session

def test_track_event(client: TestClient):
    """Test tracking a new event"""
    response = client.post("/v1/event", params={"event_name": "login", "user_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Event sent successfully!"}

def test_get_events_empty(client: TestClient):
    """Test getting events when database is empty"""
    response = client.get("/v1/events")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": []}

def test_get_events_with_data(client: TestClient, db_session: Session):
    """Test getting events with existing data"""
    # Create test events
    events = [
        Event(event_name="login", user_id=1),
        Event(event_name="purchase", user_id=1),
        Event(event_name="click", user_id=2)
    ]
    for event in events:
        db_session.add(event)
    db_session.commit()

    # Test getting all events
    response = client.get("/v1/events")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 3
    assert all(isinstance(event["user_id"], int) for event in data)

    # Test filtering by event name
    response = client.get("/v1/events", params={"event_name": "login"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["event_name"] == "login"

    # Test pagination
    response = client.get("/v1/events", params={"limit": 2, "offset": 0})
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 2

def test_invalid_event_parameters(client: TestClient):
    """Test invalid parameters for event tracking"""
    # Missing required parameters
    response = client.post("/v1/event")
    assert response.status_code == 422

    # Invalid user_id type
    response = client.post("/v1/event", params={"event_name": "login", "user_id": "invalid"})
    assert response.status_code == 422

def test_invalid_pagination_parameters(client: TestClient):
    """Test invalid pagination parameters"""
    # Negative limit
    response = client.get("/v1/events", params={"limit": -1})
    assert response.status_code == 200  # FastAPI handles this gracefully

    # Negative offset
    response = client.get("/v1/events", params={"offset": -1})
    assert response.status_code == 200  # FastAPI handles this gracefully 