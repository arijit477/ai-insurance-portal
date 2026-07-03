from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def hash_password(password: str) -> str:
    """Hash a plain text password.

    Note: bcrypt (and passlib's bcrypt handler) effectively operates on the first
    72 bytes of the password. To avoid runtime errors like:
    "password cannot be longer than 72 bytes", we explicitly truncate on the
    UTF-8 byte representation.
    """
    if password is None:
        raise ValueError("password cannot be None")

    # bcrypt limit is 72 bytes (not 72 characters).
    raw = password.encode("utf-8")
    if len(raw) > 72:
        raw = raw[:72]

    return pwd_context.hash(raw.decode("utf-8", errors="ignore"))






def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a password against its hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(
            timezone.utc
        ) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc
        ) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {"exp": expire}
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def decode_access_token(
    token: str,
):
    """
    Decode a JWT token.
    Raises JWTError if invalid.
    """

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    return payload


def create_password_reset_token(
    email: str,
) -> str:
    """
    Create password reset token.
    Valid for 15 minutes.
    """

    expire = timedelta(minutes=15)

    return create_access_token(
        data={
            "sub": email,
            "type": "password_reset",
        },
        expires_delta=expire,
    )


def verify_password_reset_token(
    token: str,
):
    """
    Verify password reset token.
    Returns email if valid.
    """

    try:
        payload = decode_access_token(token)

        if payload.get("type") != "password_reset":
            return None

        return payload.get("sub")

    except JWTError:
        return None