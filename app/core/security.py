from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

SECRET_KEY = "your-secret-key"   # move to .env in real projects
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
RESET_TOKEN_EXPIRE_MINUTES=30

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if password matches hash"""
    return pwd_context.verify(plain_password, hashed_password)







def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(email: str) -> str:
    """
    Create a password reset token with shorter expiration
    Include a token type to distinguish from access tokens
    """
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": email,           # subject (user email)
        "exp": expire,          # expiration time
        "type": "password_reset" # token type for verification
    }
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str) -> Optional[str]:
    """
    Verify a password reset token and return the email if valid
    Returns None if token is invalid, expired, or not a reset token
    """
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if this is actually a reset token
        token_type = payload.get("type")
        if token_type != "password_reset":
            return None
            
        # Get the email (subject)
        email = payload.get("sub")
        if email is None:
            return None
            
        return email
        
    except JWTError:
        # Token is invalid or expired
        return None

def verify_reset_token_with_details(token: str) -> dict:
    """
    More detailed verification that returns the full payload or error details
    Useful for debugging or when you need more information
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != "password_reset":
            return {
                "valid": False,
                "error": "Invalid token type",
                "payload": payload
            }
            
        # Check expiration
        exp = payload.get("exp")
        if exp:
            exp_time = datetime.fromtimestamp(exp)
            if exp_time < datetime.utcnow():
                return {
                    "valid": False,
                    "error": "Token expired",
                    "expired_at": exp_time.isoformat()
                }
        
        return {
            "valid": True,
            "email": payload.get("sub"),
            "expires_at": datetime.fromtimestamp(payload.get("exp")).isoformat() if payload.get("exp") else None
        }
        
    except jwt.ExpiredSignatureError:
        return {
            "valid": False,
            "error": "Token has expired"
        }
    except jwt.JWTError as e:
        return {
            "valid": False,
            "error": f"Invalid token: {str(e)}"
        }
