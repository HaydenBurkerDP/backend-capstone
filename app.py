from flask import Flask

from db import *

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://127.0.0.1:5432/backend-capstone"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


init_db(app, db)


def create_tables():
    with app.app_context():
        print("creating tables...")
        db.create_all()
        print("tables created successfully")


if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port="8086", debug=True)
