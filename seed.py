                                                                 
from sqlmodel import Session, select
from app.database import engine
from app.models.role import Role
from app.models.user import User
from app.core.security import hash_password

def seed():
    with Session(engine) as session:

                                           
        role_names = ["admin", "manager", "management", "driver"]
        role_map = {}

        for name in role_names:
            existing = session.exec(
                select(Role).where(Role.name == name)
            ).first()

            if not existing:
                role = Role(name=name, description=f"{name} role")
                session.add(role)
                session.commit()
                session.refresh(role)
                role_map[name] = role.id
                print(f"Created role: {name}")
            else:
                role_map[name] = existing.id
                print(f"Role already exists: {name}")

                                                
        admin_email = "admin@korafleet.local"
        existing_admin = session.exec(
            select(User).where(User.email == admin_email)
        ).first()

        if not existing_admin:
            admin = User(
                first_name="Admin",
                last_name="User",
                email=admin_email,
                password_hash=hash_password("admin123"),
                role_id=role_map["admin"],
                is_active=True,
                must_change_password=False,
                profile_completed=True,
            )
            session.add(admin)
            session.commit()
            print(f"created admin: {admin_email}")
        else:
            print(f"admin already exists: {admin_email}")

    print("seed complete.")


if __name__ == "__main__":
    seed()