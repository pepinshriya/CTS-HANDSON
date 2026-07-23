from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError


SECRET_KEY = "asdfghjkl"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/"
)

# bcrypt is preferred because it is intentionally slow,
# making brute-force attacks much harder than MD5 or SHA-256.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against its bcrypt hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(data: dict):
    """
    Create a JWT access token that expires in 30 minutes.
    """

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )