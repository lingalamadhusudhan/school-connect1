from app.db.database import Base, engine

# Import models so SQLAlchemy knows about every table.
import app.models  # noqa: F401


def create_tables():
    print("Creating School-Connect database tables...")

    Base.metadata.create_all(bind=engine)

    print("School-Connect database tables created successfully.")


if __name__ == "__main__":
    create_tables()