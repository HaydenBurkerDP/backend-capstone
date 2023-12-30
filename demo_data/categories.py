from db import db
from demo_data.seed_data import categories
from models.categories import Categories


def add_categories():
    for category in categories:
        name = category
        new_category = db.session.query(Categories).filter(Categories.name == name).first()

        if not new_category:
            active = True
            new_category = Categories(name, active)

            db.session.add(new_category)

    db.session.commit()
