from typing import Any
import datetime as dt
import bcrypt
import jwt

from core.config import settings

class Security:
    """Class for handling security operations."""

    @classmethod
    def verify_password(cls, password: str, hashed_password: bytes) -> bool:
        """Compares a hashed password with the password from the database."""
        return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)

    @staticmethod
    def __create_token(payload: dict[str, Any], minutes: int, now: dt.datetime) -> str:
        """Token creation."""
        to_encode = payload.copy()
        expire = now + dt.timedelta(minutes=minutes)

        to_encode.update(exp=expire, iat=now)
        return jwt.encode(
            payload=to_encode,
            key=settings.auth.private_key_path.read_text(),
            algorithm=settings.auth.algorithm,
        )

    @classmethod
    def create_access_token(cls, model_id: str, now: dt.datetime = dt.datetime.now(dt.timezone.utc)) -> str:
        """Create an access token."""
        payload = {"sub": model_id, "type": "access"}
        access_token = cls.__create_token(
            payload=payload,
            minutes=settings.auth.access_token_expire_minutes,
            now=now,
        )
        return access_token

    @classmethod
    def create_refresh_token(cls, model_id: str, now: dt.datetime = dt.datetime.now(dt.timezone.utc)) -> str:
        """Create a refresh token."""
        payload = {"sub": model_id, "type": "refresh"}
        refresh_token = cls.__create_token(
            payload=payload,
            minutes=settings.auth.refresh_token_expire_minutes,
            now=now,
        )
        return refresh_token

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Decode the token."""
        payload = jwt.decode(
            jwt=token,
            key=settings.auth.public_key_path.read_text(),
            algorithms=[settings.auth.algorithm],
        )
        return payload

    @staticmethod
    def decode_token_not_verify_signature(token: str) -> dict[str, Any]:
        """Decode the token without verifying the signature."""
        payload = jwt.decode(
            jwt=token,
            key=settings.auth.public_key_path.read_text(),
            algorithms=[settings.auth.algorithm],
            options={"verify_signature": False},
        )
        return payload

    @staticmethod
    def hash_password(password: str) -> bytes:
        """Hash the password during registration."""
        salt = bcrypt.gensalt()
        password_bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)
