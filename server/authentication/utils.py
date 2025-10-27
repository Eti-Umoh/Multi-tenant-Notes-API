import logging
from server.config import settings
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import random, string
from jose import jwt, JWTError, ExpiredSignatureError

# Get an instance of a logger
logger = logging.getLogger(__name__)

SECRET_KEY = settings.SECRET
ALGORITHM = settings.ALGORITHM


# Token generation
def create_access_token(subject: str, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# OAuth2 Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authorize_jwt_subject(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            raise HTTPException(status_code=401, detail="Token subject missing, Please Log In")
        return subject
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired, Please Log In")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token, Please Log In")


def generate_random_password(length: int = 10) -> str:
    """Generate a random alphanumeric password"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
