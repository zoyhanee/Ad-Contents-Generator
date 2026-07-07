from app.db.database import Base, engine
from app.models import AdDraft, AdProject, AdStrategy, FinalResult, Product, User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
