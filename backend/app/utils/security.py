from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError

from datetime import timedelta, datetime, timezone
from ..config import setting
from ..utils import exceptions

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password (str): Plaintext password to verify.
        hashed_password (str): Password hash produced by the configured CryptContext.

    Returns:
        bool: True if the plaintext matches the hash, otherwise False.
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password using the configured password hashing scheme.

    Args:
        password (str): Plaintext password to hash.

    Returns:
        str: Secure password hash suitable for storage.
    """
    return password_hash.hash(password)


def create_token(
    data: dict, expires_delta: timedelta | None = None, token_type: str = "access"
):
    """
    Create a signed JWT token (access or refresh).

    Notes:
        Expiration is determined by token_type using application settings.
        The expires_delta argument is currently ignored.

    Args:
        data (dict): Claims to include in the token (e.g., {"sub": "<user_id>", "role": "<role>"}).
        expires_delta (timedelta | None): Ignored; retained for compatibility.
        token_type (str): "access" or "refresh"; controls secret and expiration.

    Returns:
        str: Encoded JWT string.
    """
    to_encode = data.copy()
    expires_delta = (
        timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        if token_type == "access"
        else timedelta(days=setting.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})

    secret = (
        setting.ACCESS_SECRET_KEY
        if token_type == "access"
        else setting.REFRESH_SECRET_KEY
    )

    encoded_jwt = jwt.encode(payload=to_encode, key=secret, algorithm=setting.ALGORITHM)
    return encoded_jwt


def decode_token(token, token_type="access"):
    """
    Decode and validate a JWT token and return its payload.

    Validation:
        - Uses the appropriate secret based on token_type.
        - Ensures the 'sub' (subject) claim is present.

    Args:
        token (str): Encoded JWT to decode.
        token_type (str): "access" or "refresh"; selects the verification secret.

    Returns:
        dict: Decoded token payload.

    Raises:
        InvalidCredentialsException: If the token is invalid or missing required claims.
    """
    token_key = (
        setting.ACCESS_SECRET_KEY
        if token_type == "access"
        else setting.REFRESH_SECRET_KEY
    )

    try:
        payload = jwt.decode(jwt=token, key=token_key, algorithms=[setting.ALGORITHM])

        if payload.get("sub") is None:
            raise exceptions.InvalidCredentialsException()

    except InvalidTokenError:
        raise exceptions.InvalidCredentialsException()
    else:
        return payload