"""In-memory user store.

This is deliberately the simplest thing that works so the template runs
out of the box. Swap it for SQLAlchemy/SQLModel + a real database by
replacing these four functions — nothing else in the app needs to change.
"""

import bcrypt

# username -> {"username": str, "hashed_password": bytes, "is_active": bool}
_users: dict[str, dict] = {}


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed)
    except ValueError:
        # e.g. password longer than bcrypt's 72-byte limit
        return False


def get_user(username: str) -> dict | None:
    return _users.get(username)


def create_user(username: str, password: str) -> dict:
    user = {
        "username": username,
        "hashed_password": hash_password(password),
        "is_active": True,
    }
    _users[username] = user
    return user


def seed_demo_user() -> None:
    """Create the demo/demo1234 account used in the frontend login hint."""
    if "demo" not in _users:
        create_user("demo", "demo1234")
