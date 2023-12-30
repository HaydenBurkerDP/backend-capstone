import sys

from demo_data.users import add_users
from demo_data.categories import add_categories


def run_demo_data():
    if len(sys.argv) > 1 and sys.argv[1] == "demo-data":
        print("creating demo data...")

        add_users()
        add_categories()
