# Goals Tracker Backend

### Setup

Create a .env file in the root folder and add in the following lines

    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = "8086"

    DATABASE_SCHEME = "postgresql://"
    DATABASE_USER = "<your name here>"
    DATABASE_ADDRESS = "127.0.0.1"
    DATABASE_PORT = "5432"
    DATABASE_NAME = "backend-capstone"

Change the value of DATABASE_USER to your name

### Steps to run

    python3 -m pipenv shell
    pipenv install
    python app.py

### To create demo data, run

    python app.py demo-data
