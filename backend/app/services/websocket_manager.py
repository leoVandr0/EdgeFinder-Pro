"""
WebSocket Connection Manager
Handles real-time price updates and data streaming to connected clients
"""
from fastapi import WebSocket
from typing import List, Dict, Set
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts updates to clients
    """

    def __init__(self):
        # Active connections by channel
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "forex": set(),
            "indices": set(),
            "strength": set(),
            "all": set()
        }

    async def connect(self, websocket: WebSocket, channel: str = "all"):
        """
        Accept a new WebSocket connection and add to channel
        """
        await websocket.accept()

        if channel not in self.active_connections:
            self.active_connections[channel] = set()

        self.active_connections[channel].add(websocket)
        print(f"Client connected to channel '{channel}'. Total: {len(self.active_connections[channel])}")

    def disconnect(self, websocket: WebSocket, channel: str = "all"):
        """
        Remove a WebSocket connection from channel
        """
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
            print(f"Client disconnected from channel '{channel}'. Total: {len(self.active_connections[channel])}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send a message to a specific client
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")

    async def broadcast(self, message: dict, channel: str = "all"):
        """
        Broadcast a message to all clients in a channel
        """
        if channel not in self.active_connections:
            return

        disconnected = set()

        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                disconnected.add(connection)

        # Remove disconnected clients
        for connection in disconnected:
            self.active_connections[channel].discard(connection)

    async def broadcast_to_all_channels(self, message: dict):
        """
        Broadcast a message to all channels
        """
        for channel in self.active_connections.keys():
            await self.broadcast(message, channel)

    def get_connection_count(self, channel: str = None) -> int:
        """
        Get the number of active connections
        """
        if channel:
            return len(self.active_connections.get(channel, set()))
        return sum(len(connections) for connections in self.active_connections.values())


# Global connection manager instance
manager = ConnectionManager()


async def broadcast_price_updates():
    """
    Background task to broadcast price updates every few seconds
    This runs continuously and sends updates to all connected clients
    """
    from app.services.forex_data import get_real_forex_rates, get_real_currency_strength
    from app.services.indices_data import get_real_indices_data

    while True:
        try:
            # Fetch latest data
            forex_rates = await get_real_forex_rates()
            currency_strength = await get_real_currency_strength()
            indices_data = await get_real_indices_data()

            # Broadcast forex updates
            if forex_rates and manager.get_connection_count("forex") > 0:
                await manager.broadcast({
                    "type": "forex_update",
                    "data": forex_rates,
                    "timestamp": datetime.utcnow().isoformat()
                }, "forex")

            # Broadcast indices updates
            if indices_data and manager.get_connection_count("indices") > 0:
                await manager.broadcast({
                    "type": "indices_update",
                    "data": indices_data,
                    "timestamp": datetime.utcnow().isoformat()
                }, "indices")

            # Broadcast currency strength updates
            if currency_strength and manager.get_connection_count("strength") > 0:
                await manager.broadcast({
                    "type": "strength_update",
                    "data": currency_strength,
                    "timestamp": datetime.utcnow().isoformat()
                }, "strength")

            # Broadcast to "all" channel
            if manager.get_connection_count("all") > 0:
                await manager.broadcast({
                    "type": "market_update",
                    "data": {
                        "forex": forex_rates,
                        "indices": indices_data,
                        "strength": currency_strength
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }, "all")

        except Exception as e:
            print(f"Error in broadcast_price_updates: {e}")

        # Wait 5 seconds before next update
        await asyncio.sleep(5)
