"""
In-memory user storage
In production, replace this with a real database (MongoDB, PostgreSQL, etc.)
"""
from typing import Dict, Optional, List
from datetime import datetime
import uuid

# In-memory storage
users_db: Dict[str, dict] = {}
watchlists_db: Dict[str, List[str]] = {}  # user_id -> list of pairs


class UserStore:
    """User storage and management"""

    @staticmethod
    def create_user(email: str, username: str, hashed_password: str) -> dict:
        """Create a new user"""
        user_id = str(uuid.uuid4())

        user = {
            "id": user_id,
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }

        users_db[user_id] = user
        watchlists_db[user_id] = []  # Initialize empty watchlist

        return user

    @staticmethod
    def get_user_by_email(email: str) -> Optional[dict]:
        """Get user by email"""
        for user in users_db.values():
            if user["email"] == email:
                return user
        return None

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[dict]:
        """Get user by ID"""
        return users_db.get(user_id)

    @staticmethod
    def get_user_by_username(username: str) -> Optional[dict]:
        """Get user by username"""
        for user in users_db.values():
            if user["username"] == username:
                return user
        return None


class WatchlistStore:
    """Watchlist storage and management"""

    @staticmethod
    def get_watchlist(user_id: str) -> List[str]:
        """Get user's watchlist"""
        return watchlists_db.get(user_id, [])

    @staticmethod
    def add_to_watchlist(user_id: str, pair: str) -> List[str]:
        """Add a pair to watchlist"""
        if user_id not in watchlists_db:
            watchlists_db[user_id] = []

        pair = pair.upper()
        if pair not in watchlists_db[user_id]:
            watchlists_db[user_id].append(pair)

        return watchlists_db[user_id]

    @staticmethod
    def remove_from_watchlist(user_id: str, pair: str) -> List[str]:
        """Remove a pair from watchlist"""
        if user_id in watchlists_db:
            pair = pair.upper()
            if pair in watchlists_db[user_id]:
                watchlists_db[user_id].remove(pair)

        return watchlists_db.get(user_id, [])

    @staticmethod
    def clear_watchlist(user_id: str):
        """Clear entire watchlist"""
        watchlists_db[user_id] = []
