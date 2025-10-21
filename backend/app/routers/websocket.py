from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager
import json

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for all real-time updates (forex, indices, strength)

    Connect to: ws://localhost:8000/ws
    """
    await manager.connect(websocket, "all")

    try:
        # Send initial connection message
        await manager.send_personal_message({
            "type": "connection",
            "message": "Connected to Richy's Board WebSocket",
            "channels": ["forex", "indices", "strength"]
        }, websocket)

        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()

            # Echo back for debugging
            await manager.send_personal_message({
                "type": "echo",
                "message": f"Received: {data}"
            }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, "all")
        print("Client disconnected from all channels")


@router.websocket("/ws/forex")
async def websocket_forex(websocket: WebSocket):
    """
    WebSocket endpoint for forex price updates only

    Connect to: ws://localhost:8000/ws/forex
    """
    await manager.connect(websocket, "forex")

    try:
        await manager.send_personal_message({
            "type": "connection",
            "message": "Connected to Forex updates",
            "channel": "forex"
        }, websocket)

        while True:
            data = await websocket.receive_text()
            # Handle ping/pong for keep-alive
            if data == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, "forex")
        print("Client disconnected from forex channel")


@router.websocket("/ws/indices")
async def websocket_indices(websocket: WebSocket):
    """
    WebSocket endpoint for stock indices updates only

    Connect to: ws://localhost:8000/ws/indices
    """
    await manager.connect(websocket, "indices")

    try:
        await manager.send_personal_message({
            "type": "connection",
            "message": "Connected to Indices updates",
            "channel": "indices"
        }, websocket)

        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, "indices")
        print("Client disconnected from indices channel")


@router.websocket("/ws/strength")
async def websocket_strength(websocket: WebSocket):
    """
    WebSocket endpoint for currency strength updates only

    Connect to: ws://localhost:8000/ws/strength
    """
    await manager.connect(websocket, "strength")

    try:
        await manager.send_personal_message({
            "type": "connection",
            "message": "Connected to Currency Strength updates",
            "channel": "strength"
        }, websocket)

        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, "strength")
        print("Client disconnected from strength channel")
