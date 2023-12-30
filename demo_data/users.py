from flask_bcrypt import generate_password_hash

from db import db
from demo_data.seed_data import users
from models.users import Users


def add_users():
    for user in users:
        first_name, last_name = user.split(" ")
        email = f"{first_name.lower()}_{last_name.lower()}@test.com"

        new_user = db.session.query(Users).filter(Users.email == email).first()

        if not new_user:
            password = "1234"
            role = "user"
            active = True

            password = generate_password_hash(password).decode("utf8")
            new_user = Users(first_name, last_name, email, password, role, active)
            db.session.add(new_user)

    db.session.commit()
