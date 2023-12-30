from flask import jsonify

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from models.categories import Categories
from models.goal_logs import GoalLogs, goal_log_schema, goal_logs_schema
from models.goals import Goals
from models.users import Users


@authenticate_return_auth
def goal_log_add(req, auth_info):
    post_data = req.form if req.form else req.json
    goal_id = post_data.get("goal_id")
    goal_query = None

    if goal_id:
        if not validate_uuid4(goal_id):
            return jsonify({"message": "invalid goal id"}), 400

        goal_query = db.session.query(Goals).filter(Goals.goal_id == goal_id).first()

        if not goal_query:
            return jsonify({"message": "goal not found"}), 404

    category_ids = post_data.get("category_ids")
    if category_ids:
        post_data.pop("category_ids")

    new_goal_log = GoalLogs.get_new_goal_log()
    populate_object(new_goal_log, post_data)
    new_goal_log.user_id = auth_info.user_id

    if goal_id:
        for category in goal_query.categories:
            new_goal_log.categories.append(category)

    elif category_ids:
        for category_id in category_ids:
            if not validate_uuid4(category_id):
                return jsonify({"message": "invalid category id"}), 400

        categories_query = db.session.query(Categories).filter(Categories.category_id.in_(category_ids)).all()

        for category in categories_query:
            if not category:
                return jsonify({"message": "category not found"}), 404

            new_goal_log.categories.append(category)

    if goal_query:
        new_goal_log.name = goal_query.name
        new_goal_log.description = goal_query.description

    db.session.add(new_goal_log)
    db.session.commit()

    return jsonify({"message": "goal log added", "goal_log": goal_log_schema.dump(new_goal_log)}), 201


@authenticate
def goal_log_get_by_id(req, goal_log_id):
    if not validate_uuid4(goal_log_id):
        return jsonify({"message": "invalid goal log id"}), 400

    goal_log_query = db.session.query(GoalLogs).filter(GoalLogs.goal_log_id == goal_log_id).first()

    if not goal_log_query:
        return jsonify({"message": "goal log not found"}), 404

    else:
        return jsonify({"message": "goal log found", "goal_log": goal_log_schema.dump(goal_log_query)}), 200


@authenticate_return_auth
def goal_logs_get_all(req, auth_info):
    if auth_info.user.role != "super-admin":
        return jsonify({"message": "unauthorized"}), 403

    goal_logs_query = db.session.query(GoalLogs).all()

    return jsonify({"message": "goal logs found", "goal_logs": goal_logs_schema.dump(goal_logs_query)}), 200


@authenticate_return_auth
def goal_logs_get_from_auth_info(req, auth_info):
    goal_logs_query = db.session.query(GoalLogs).filter(GoalLogs.user_id == auth_info.user_id).all()

    return jsonify({"message": "goal logs found", "goal_logs": goal_logs_schema.dump(goal_logs_query)}), 200


@authenticate_return_auth
def goal_log_update_by_id(req, goal_log_id, auth_info):
    if not validate_uuid4(goal_log_id):
        return jsonify({"message": "invalid goal log id"}), 400

    post_data = req.form if req.form else req.json

    goal_log_query = db.session.query(GoalLogs).filter(GoalLogs.goal_log_id == goal_log_id).first()

    if not goal_log_query:
        return jsonify({"message": "goal log not found"}), 404

    if goal_log_query.user_id != auth_info.user_id and auth_info.user.role != "super-admin":
        return jsonify({"message": "unauthorized"}), 403

    category_ids = post_data.get("category_ids")
    if "category_ids" in post_data:
        post_data.pop("category_ids")

    user_id = post_data.get("user_id")
    if "user_id" in post_data:
        if user_id != str(auth_info.user_id) and auth_info.user.role != "super-admin":
            return jsonify({"message": "cannot change user id"}), 400

        if not validate_uuid4(user_id):
            return jsonify({"message": "invalid user id"}), 400

        user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

        if not user_query:
            return jsonify({"message": "user not found"}), 404

    goal_id = post_data.get("goal_id")
    if "goal_id" in post_data:
        return jsonify({"message": "cannot change goal id"}), 403

    populate_object(goal_log_query, post_data)

    if category_ids:
        for category_id in category_ids:
            if not validate_uuid4(category_id):
                return jsonify({"message": "invalid category id"}), 400

        categories_query = db.session.query(Categories).filter(Categories.category_id.in_(category_ids)).all()

        for category in categories_query:
            if not category:
                return jsonify({"message": "category not found"}), 404

            if category in goal_log_query.categories:
                goal_log_query.categories.pop(goal_log_query.categories.index(category))

            else:
                goal_log_query.categories.append(category)

    db.session.commit()

    return jsonify({"message": "goal log updated", "goal_log": goal_log_schema.dump(goal_log_query)}), 200


@authenticate_return_auth
def goal_log_delete_by_id(req, goal_log_id, auth_info):
    if not validate_uuid4(goal_log_id):
        return jsonify({"message": "invalid goal log id"}), 400

    goal_log_query = db.session.query(GoalLogs).filter(GoalLogs.goal_log_id == goal_log_id).first()

    if not goal_log_query:
        return jsonify({"message": "goal log not found"}), 404

    if goal_log_query.user_id != auth_info.user_id and auth_info.user.role != "super-admin":
        return jsonify({"message": "unauthorized"}), 403

    db.session.delete(goal_log_query)
    db.session.commit()

    return jsonify({"message": "goal log deleted"}), 200
