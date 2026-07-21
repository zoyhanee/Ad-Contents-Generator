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


def get_user_by_provider(
    db: Session,
    provider: str,
    provider_user_id: str,
) -> User | None:
    return (
        db.query(User)
        .filter(
            User.provider == provider,
            User.provider_user_id == provider_user_id,
        )
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


def create_oauth_user(
    db: Session,
    email: str,
    provider: str,
    provider_user_id: str,
    store_name: str | None = None,
) -> User:
    db_user = User(
        email=email,
        password_hash=None,
        provider=provider,
        provider_user_id=provider_user_id,
        store_name=store_name,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def link_oauth_provider(
    db: Session,
    user: User,
    provider_user_id: str,
) -> User:
    user.provider_user_id = provider_user_id
    db.commit()
    db.refresh(user)

    return user
