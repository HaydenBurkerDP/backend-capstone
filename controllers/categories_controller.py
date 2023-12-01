from flask import jsonify

from db import db
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from models.categories import Categories, category_schema, categories_schema


@authenticate_return_auth
def category_add(req, auth_info):
    if auth_info.user.role not in ["super-admin", "admin"]:
        return jsonify({"message": "unauthorized"}), 403

    post_data = req.form if req.form else req.json

    new_category = Categories.get_new_category()
    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "category added", "category": category_schema.dump(new_category)}), 201


@authenticate_return_auth
def category_get_by_id(req, category_id, auth_info):
    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id)

    if auth_info.user.role != "super-admin":
        category_query = category_query.filter(Categories.active == True)

    category_query = category_query.first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    else:
        return jsonify({"message": "category found", "category": category_schema.dump(category_query)}), 200


@authenticate_return_auth
def categories_get_all(req, auth_info):
    categories_query = db.session.query(Categories)

    if auth_info.user.role != "super-admin":
        categories_query = categories_query.filter(Categories.active == True)

    categories_query = categories_query.all()

    return jsonify({"message": "categories found", "categories": categories_schema.dump(categories_query)}), 200


@authenticate_return_auth
def category_update_by_id(req, category_id, auth_info):
    if auth_info.user.role not in ["super-admin", "admin"]:
        return jsonify({"message": "unauthorized"}), 403

    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400

    post_data = req.form if req.form else req.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    populate_object(category_query, post_data)
    db.session.commit()

    return jsonify({"message": "category updated", "category": category_schema.dump(category_query)}), 200


@authenticate_return_auth
def category_activity(req, category_id, auth_info):
    if auth_info.user.role not in ["super-admin", "admin"]:
        return jsonify({"message": "unauthorized"}), 403

    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    category_query.active = not category_query.active
    db.session.commit()

    if category_query.active:
        return jsonify({"message": "category activated", "category": category_schema.dump(category_query)}), 200
    else:
        return jsonify({"message": "category deactivated", "category": category_schema.dump(category_query)}), 200


@authenticate_return_auth
def category_delete_by_id(req, category_id, auth_info):
    if auth_info.user.role != "super-admin":
        return jsonify({"message": "unauthorized"}), 403

    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    db.session.delete(category_query)
    db.session.commit()

    return jsonify({"message": "category deleted"}), 200
