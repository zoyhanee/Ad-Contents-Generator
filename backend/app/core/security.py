from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """비밀번호를 안전하게 해시한다."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해시를 비교한다."""
    return password_hasher.verify(password, hashed_password)