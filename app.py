from flask import Flask
from flask_bcrypt import generate_password_hash
from flask_cors import CORS
import os

from db import *
from util.blueprints import register_blueprints
from models.users import Users
from demo_data.demo_data import run_demo_data

app = Flask(__name__)

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_PORT")

database_schema = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")


app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_schema}{database_user}@{database_address}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


init_db(app, db)


def create_super_admin():
    print("Querying for Super Admin...")
    user = db.session.query(Users).filter(Users.role == "super-admin").first()

    if not user:
        print("Super Admin not found! Creating new user")
        first_name = "Super"
        last_name = "Admin"
        email = "super-admin@test.com"
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
        run_demo_data()


CORS(app)
register_blueprints(app)

if __name__ == "__main__":
    create_tables()
    app.run(host=flask_host, port=flask_port, debug=True)
