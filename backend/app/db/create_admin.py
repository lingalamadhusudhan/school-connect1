import getpass

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.role import Role
from app.models.user import User


def create_admin():
    db = SessionLocal()

    try:
        role = (
            db.query(Role)
            .filter(Role.name == "ADMIN")
            .first()
        )

        if not role:
            print("ADMIN role does not exist.")
            print("Run: python -m app.db.seed")
            return

        email = input("Admin email: ").strip().lower()
        full_name = input("Admin full name: ").strip()

        password = getpass.getpass(
            "Admin password: "
        )

        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return

        existing = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing:
            print("Admin/user already exists.")
            return

        admin = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role_id=role.id,
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print("School-Connect Admin created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()