from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from util.reflection import populate_object
from models.users import Users, user_schema, users_schema


def user_add(req):
    post_data = req.form if req.form else req.json

    new_user = Users.get_new_user()
    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user added", "user": user_schema.dump(new_user)}), 201


def user_get_by_id(req, user_id):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    else:
        return jsonify({"message": "user found", "user": user_schema.dump(user_query)}), 200


def users_get_all(req):
    users_query = db.session.query(Users).all()

    return jsonify({"message": "users found", "users": users_schema.dump(users_query)}), 200


def user_update_by_id(req, user_id):
    post_data = req.form if req.form else req.json

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    populate_object(user_query, post_data)

    if post_data.get("password"):
        user_query.password = generate_password_hash(user_query.password).decode("utf8")

    db.session.commit()

    return jsonify({"message": "user updated", "user": user_schema.dump(user_query)}), 200


def user_activity(req, user_id):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    user_query.active = not user_query.active
    db.session.commit()

    if user_query.active:
        return jsonify({"message": "user activated", "user": user_schema.dump(user_query)}), 200

    else:
        return jsonify({"message": "user deactivated", "user": user_schema.dump(user_query)}), 200


def user_delete_by_id(req, user_id):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    db.session.delete(user_query)
    db.session.commit()

    return jsonify({"message": "user deleted"}), 200
