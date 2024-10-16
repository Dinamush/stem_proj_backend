# create_superuser.py
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import get_password_hash
from datetime import date

def create_superuser():
    db: Session = SessionLocal()
    try:
        email = input("Enter email for superuser: ")
        password = input("Enter password for superuser: ")
        hashed_password = get_password_hash(password)

        superuser = User(
            first_name="Admin",
            last_name="User",
            birth_date=date(1990, 1, 1),
            email=email,
            hashed_password=hashed_password,
            phone_number="1234567890",
            competition="AdminCompetition",
            agreed_to_rules=True,
            is_active=True,
            is_superuser=True
        )

        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        print(f"Superuser '{email}' created successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error creating superuser: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser()

# Enter email for superuser: admin@keen360.com
# Enter password for superuser: admin123