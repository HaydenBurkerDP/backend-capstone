from flask import Flask
from flask_bcrypt import generate_password_hash

from db import *
from util.blueprints import register_blueprints
from models.users import Users

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://127.0.0.1:5432/backend-capstone"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


init_db(app, db)


def create_super_admin():
    print("Querying for Super Admin...")
    user = db.session.query(Users).filter(Users.role == "super-admin").first()

    if not user:
        print("Super Admin not found! Creating new user")
        first_name = "Super"
        last_name = "Admin"
        email = input("Enter an email for the Super Admin: ")
        password = input("Enter a password for the Super Admin: ")
        role = "super-admin"
        active = True

        password = generate_password_hash(password).decode("utf8")

        new_user = Users(first_name, last_name, email, password, role, active)

        db.session.add(new_user)
        db.session.commit()

    else:
        print("Super Admin found!")


def create_tables():
    with app.app_context():
        print("creating tables...")
        db.create_all()
        print("tables created successfully")

        create_super_admin()


register_blueprints(app)


if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port="8086", debug=True)
