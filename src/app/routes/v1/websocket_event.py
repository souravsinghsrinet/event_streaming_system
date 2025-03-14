from fastapi import (
    APIRouter, Depends, status,
    WebSocket, WebSocketDisconnect
)
from src.app.services.websocket_service import active_connections

websocket_event_router = APIRouter(
    prefix="/v1",
    tags=["websocket_event"],
    responses={
        404: {"description": "Not found"}
    }
)



@websocket_event_router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        active_connections.remove(websocket)


