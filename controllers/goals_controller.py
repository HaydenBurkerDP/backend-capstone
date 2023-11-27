from flask import jsonify

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from models.goals import Goals, goal_schema, goals_schema
from models.goals_categories_xref import goals_categories_association_table
from models.users_goals_xref import users_goals_association_table


@authenticate_return_auth
def goal_add(req, auth_info):
    post_data = req.form if req.form else req.json

    new_goal = Goals.get_new_goal()
    populate_object(new_goal, post_data)
    new_goal.creator_id = auth_info.user_id

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"message": "goal added", "goal": goal_schema.dump(new_goal)}), 201


@authenticate
def goal_get_by_id(req, goal_id):
    if not validate_uuid4(goal_id):
        return jsonify({"message": "invalid goal id"}), 400

    goal_query = db.session.query(Goals).filter(Goals.goal_id == goal_id).first()

    if not goal_query:
        return jsonify({"message": "goal not found"}), 404

    else:
        return jsonify({"message": "goal found", "goal": goal_schema.dump(goal_query)}), 200


@authenticate
def goals_get_all(req):
    goals_query = db.session.query(Goals).all()

    return jsonify({"message": "goals found", "goals": goals_schema.dump(goals_query)}), 200


@authenticate_return_auth
def goals_get_by_category_id(req, category_id, auth_info):
    if not validate_uuid4(category_id):
        return jsonify({"message": "invalid category id"}), 400

    goals_query = db.session.query(Goals)\
        .join(goals_categories_association_table)\
        .join(users_goals_association_table)\
        .filter(goals_categories_association_table.columns.get("category_id") == category_id)\
        .filter(users_goals_association_table.columns.get("user_id") == auth_info.user_id)\
        .all()

    return jsonify({"message": "goals found", "goals": goals_schema.dump(goals_query)}), 200


@authenticate_return_auth
def goal_update_by_id(req, goal_id, auth_info):
    if not validate_uuid4(goal_id):
        return jsonify({"message": "invalid goal id"}), 400

    post_data = req.form if req.form else req.json

    goal_query = db.session.query(Goals).filter(Goals.goal_id == goal_id).first()

    if not goal_query:
        return jsonify({"message": "goal not found"}), 404

    populate_object(goal_query, post_data)
    goal_query.creator_id = auth_info.user_id
    db.session.commit()

    return jsonify({"message": "goal updated", "goal": goal_schema.dump(goal_query)}), 200


@authenticate
def goal_delete_by_id(req, goal_id):
    if not validate_uuid4(goal_id):
        return jsonify({"message": "invalid goal id"}), 400

    goal_query = db.session.query(Goals).filter(Goals.goal_id == goal_id).first()

    if not goal_query:
        return jsonify({"message": "goal not found"}), 404

    db.session.delete(goal_query)
    db.session.commit()

    return jsonify({"message": "goal deleted"}), 200
