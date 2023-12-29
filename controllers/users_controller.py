from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from models.users import Users, user_schema, users_schema


@authenticate_return_auth
def user_add(req, auth_info):
    if auth_info.user.role != "super-admin":
        return jsonify({"message": "unauthorized"}), 403

    post_data = req.form if req.form else req.json

    fields = ["email", "password"]

    for field in fields:
        if field not in post_data or not post_data[field]:
            return jsonify({"message": f"{field} is required"}), 400

    role = post_data.get("role")

    if "role" in post_data and role not in ["super-admin", "admin", "user"]:
        return jsonify({"message": "invalid role"}), 400

    new_user = Users.get_new_user()
    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    db.session.add(new_user)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to add user"}), 400

    return jsonify({"message": "user added", "user": user_schema.dump(new_user)}), 201


@authenticate_return_auth
def user_get_by_id(req, user_id, auth_info):
    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query or (auth_info.user.role != "super-admin" and user_query.active == False):
        return jsonify({"message": "user not found"}), 404

    else:
        return jsonify({"message": "user found", "user": user_schema.dump(user_query)}), 200


@authenticate_return_auth
def user_get_from_auth_token(req, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    return jsonify({"message": "user found", "user": user_schema.dump(user_query)}), 200


@authenticate_return_auth
def users_get_all(req, auth_info):
    users_query = db.session.query(Users)

    if auth_info.user.role != "super-admin":
        users_query = users_query.filter(Users.active == True)

    users_query = users_query.all()

    return jsonify({"message": "users found", "users": users_schema.dump(users_query)}), 200


@authenticate_return_auth
def user_update_by_id(req, user_id, auth_info):
    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400

    if user_id != str(auth_info.user_id) and auth_info.user.role != "super-admin":
        return jsonify({"message": "unauthorized"}), 403

    post_data = req.form if req.form else req.json

    fields = ["email", "password"]

    for field in fields:
        if field in post_data and not post_data[field]:
            return jsonify({"message": f"invalid {field}"}), 400

    active = post_data.get("active")
    role = post_data.get("role")

    if "role" in post_data and role not in ["super-admin", "admin", "user"]:
        return jsonify({"message": "invalid role"}), 400

    if user_id == str(auth_info.user_id):
        if "active" in post_data and active == False:
            return jsonify({"message": "cannot deactivate yourself"}), 403

        if "role" in post_data and role != auth_info.user.role:
            return jsonify({"message": "cannot change your role"}), 403

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    populate_object(user_query, post_data)

    if post_data.get("password"):
        user_query.password = generate_password_hash(user_query.password).decode("utf8")

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to update user"}), 400

    return jsonify({"message": "user updated", "user": user_schema.dump(user_query)}), 200


@authenticate_return_auth
def user_activity(req, user_id, auth_info):
    if auth_info.user.role not in ["super-admin", "admin"]:
        return jsonify({"message": "unauthorized"}), 403

    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400

    if user_id == str(auth_info.user_id):
        return jsonify({"message": "cannot deactivate yourself"}), 403

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    if auth_info.user.role == "admin" and user_query.role in ["super-admin", "admin"]:
        return jsonify({"message": "unauthorized"}), 403

    user_query.active = not user_query.active
    db.session.commit()

    if user_query.active:
        return jsonify({"message": "user activated", "user": user_schema.dump(user_query)}), 200

    else:
        return jsonify({"message": "user deactivated", "user": user_schema.dump(user_query)}), 200


@authenticate_return_auth
def user_delete_by_id(req, user_id, auth_info):
    if auth_info.user.role != "super-admin":
        return jsonify({"message": "unauthorized"}), 403

    if not validate_uuid4(user_id):
        return jsonify({"message": "invalid user id"}), 400

    if user_id == str(auth_info.user_id):
        return jsonify({"message": "cannot delete yourself"}), 403

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    db.session.delete(user_query)

    try:
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete user"}), 400

    return jsonify({"message": "user deleted"}), 200
