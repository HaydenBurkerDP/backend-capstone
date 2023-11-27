from flask import jsonify
import json

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from models.goal_logs import GoalLogs, goal_log_schema, goal_logs_schema
from models.goals import Goals


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

    new_goal_log = GoalLogs.get_new_goal_log()
    populate_object(new_goal_log, post_data)
    new_goal_log.user_id = auth_info.user_id

    if goal_query:
        new_goal_log.name = goal_query.name
        new_goal_log.description = goal_query.description

    db.session.add(new_goal_log)
    db.session.commit()

    return jsonify({"message": "goal log added", "goal_log": goal_log_schema.dump(new_goal_log)}), 201


def goal_log_get_by_id(req, goal_log_id):
    if not validate_uuid4(goal_log_id):
        return jsonify({"message": "invalid goal log id"}), 400

    goal_log_query = db.session.query(GoalLogs).filter(GoalLogs.goal_log_id == goal_log_id).first()

    if not goal_log_query:
        return jsonify({"message": "goal log not found"}), 404

    else:
        return jsonify({"message": "goal log found", "goal_log": goal_log_schema.dump(goal_log_query)}), 200


def goal_logs_get_all(req):
    goal_logs_query = db.session.query(GoalLogs).all()

    return jsonify({"message": "goal logs found", "goal_logs": goal_logs_schema.dump(goal_logs_query)}), 200


def goal_log_update_by_id(req, goal_log_id):
    if not validate_uuid4(goal_log_id):
        return jsonify({"message": "invalid goal log id"}), 400

    post_data = req.form if req.form else req.json

    goal_log_query = db.session.query(GoalLogs).filter(GoalLogs.goal_log_id == goal_log_id).first()

    if not goal_log_query:
        return jsonify({"message": "goal log not found"}), 404

    populate_object(goal_log_query, post_data)
    db.session.commit()

    return jsonify({"message": "goal log updated", "goal_log": goal_log_schema.dump(goal_log_query)}), 200


def goal_log_delete_by_id(req, goal_log_id):
    if not validate_uuid4(goal_log_id):
        return jsonify({"message": "invalid goal log id"}), 400

    goal_log_query = db.session.query(GoalLogs).filter(GoalLogs.goal_log_id == goal_log_id).first()

    if not goal_log_query:
        return jsonify({"message": "goal log not found"}), 404

    db.session.delete(goal_log_query)
    db.session.commit()

    return jsonify({"message": "goal log deleted"}), 200
