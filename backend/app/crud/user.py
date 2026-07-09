from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def create_user(
    db: Session,
    user: UserCreate,
    password_hash: str,
) -> User:

    db_user = User(
        email=user.email,
        password_hash=password_hash,
        store_name=user.store_name,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user