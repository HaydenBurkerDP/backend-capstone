# Goals Tracker Backend

### Setup

Create a .env file in the root folder and add in the following lines

    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = "8086"

    DATABASE_URI = "postgresql://<your name here>@127.0.0.1:5432/backend-capstone"

Replace <your name herer> to your name

### Steps to run

    python3 -m pipenv shell
    pipenv install
    python app.py

### To create demo data, run

    python app.py demo-data
