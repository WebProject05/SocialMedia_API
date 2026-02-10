import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(password: str):
    """Hash a password using SHA256 first, then bcrypt.
    
    This approach handles passwords longer than bcrypt's 72-byte limit by
    first converting them to a fixed-length SHA256 hash (64 bytes).
    """
    sha256_hash = hashlib.sha256(password.encode("utf-8")).digest()
    return pwd_context.hash(sha256_hash)


def verify(password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password.
    
    The password must be hashed with SHA256 first to match the hash() function.
    """
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)