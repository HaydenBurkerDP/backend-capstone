from flask import Blueprint, request

import controllers

auth = Blueprint("auth", __name__)


@auth.route("/user/auth", methods=["POST"])
def auth_token_add():
    return controllers.auth_token_add(request)


@auth.route("/user/logout", methods=["PUT"])
def auth_token_remove():
    return controllers.auth_token_remove(request)
