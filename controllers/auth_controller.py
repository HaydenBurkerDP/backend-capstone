from flask import jsonify
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta

from db import db
from lib.authenticate import authenticate_return_auth
from models.auth_tokens import AuthTokens, auth_token_schema
from models.users import Users


def auth_token_add(req):
    post_data = req.form if req.form else req.json

    email = post_data.get("email")

    if not email:
        return jsonify({"message": "email is required"}), 400

    password = post_data.get("password")

    if not password:
        return jsonify({"message": "password is required"}), 400

    user_query = db.session.query(Users).filter(Users.email == email).first()

    if not user_query:
        return jsonify({"message": "invalid login"}), 401

    valid_password = check_password_hash(user_query.password, password)

    if not valid_password:
        return jsonify({"message": "invalid login"}), 401

    if not user_query.active:
        return jsonify({"message": "account has been deactivated"}), 403

    existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_query.user_id).all()

    for token in existing_tokens:
        if token.expiration < datetime.now():
            db.session.delete(token)

    expiry = datetime.now() + timedelta(hours=12)

    new_token = AuthTokens(user_query.user_id, expiry)

    db.session.add(new_token)
    db.session.commit()

    return jsonify({"auth_info": auth_token_schema.dump(new_token)}), 201


@authenticate_return_auth
def auth_token_remove(req, auth_info):
    db.session.delete(auth_info)
    db.session.commit()
    return jsonify({"message": "user logged out"}), 200
