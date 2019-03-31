from hashlib import sha512
from secrets import token_hex


def encrypt(text: str) -> str:
    return sha512(text.encode()).hexdigest()


def create_token() -> str:
    return token_hex(50)
