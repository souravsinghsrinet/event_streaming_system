import pytest
from fastapi.testclient import TestClient
from src.app.services.websocket_service import active_connections
import json

def test_websocket_connection(client: TestClient):
    """Test WebSocket connection establishment"""
    with client.websocket_connect("/v1/ws/events") as websocket:
        # Connection should be established
        assert websocket in active_connections

def test_websocket_disconnection(client: TestClient):
    """Test WebSocket disconnection"""
    with client.websocket_connect("/v1/ws/events") as websocket:
        # Connection should be established
        assert websocket in active_connections
        # Close the connection
        websocket.close()
        # Connection should be removed
        assert websocket not in active_connections

def test_websocket_message_reception(client: TestClient, db_session):
    """Test receiving messages through WebSocket"""
    with client.websocket_connect("/v1/ws/events") as websocket:
        # Send a test event
        test_event = {"event": "test_event", "user_id": 1}
        client.post("/v1/event", params=test_event)
        
        # Receive the message
        data = websocket.receive_json()
        assert data == test_event

def test_multiple_websocket_connections(client: TestClient):
    """Test multiple simultaneous WebSocket connections"""
    with client.websocket_connect("/v1/ws/events") as websocket1, \
         client.websocket_connect("/v1/ws/events") as websocket2:
        # Both connections should be established
        assert websocket1 in active_connections
        assert websocket2 in active_connections
        
        # Send a test event
        test_event = {"event": "test_event", "user_id": 1}
        client.post("/v1/event", params=test_event)
        
        # Both connections should receive the message
        data1 = websocket1.receive_json()
        data2 = websocket2.receive_json()
        assert data1 == test_event
        assert data2 == test_event

def test_websocket_connection_cleanup(client: TestClient):
    """Test WebSocket connection cleanup on error"""
    with pytest.raises(Exception):
        with client.websocket_connect("/v1/ws/events") as websocket:
            # Simulate a connection error
            raise Exception("Connection error")
    
    # Connection should be cleaned up even after error
    assert websocket not in active_connections 