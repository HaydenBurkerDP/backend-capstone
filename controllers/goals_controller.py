from flask import jsonify

from db import db
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object
from util.validate_uuid4 import validate_uuid4
from models.goals import Goals, goal_schema, goals_schema
from models.categories import Categories
from models.goals_categories_xref import goals_categories_association_table
from models.users import Users
from models.users_goals_xref import users_goals_association_table


@authenticate_return_auth
def goal_add(req, auth_info):
    post_data = req.form if req.form else req.json

    category_ids = post_data.get("category_ids")
    if category_ids:
        post_data.pop("category_ids")

    new_goal = Goals.get_new_goal()
    populate_object(new_goal, post_data)
    new_goal.creator_id = auth_info.user_id
    new_goal.users.append(auth_info.user)

    if category_ids:
        for category_id in category_ids:
            if not validate_uuid4(category_id):
                return jsonify({"message": "invalid category id"}), 400

        categories_query = db.session.query(Categories).filter(Categories.category_id.in_(category_ids)).all()

        for category in categories_query:
            if not category:
                return jsonify({"message": "category not found"}), 404

            new_goal.categories.append(category)

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
def goals_get_from_auth_token(req, auth_info):
    goals_query = db.session.query(Goals).filter(Goals.creator_id == auth_info.user_id).all()

    return jsonify({"message": "goals found", "goals": goals_schema.dump(goals_query)}), 200


@authenticate_return_auth
def goals_get_shared(req, auth_info):
    goals_query = db.session.query(Goals)\
        .join(users_goals_association_table)\
        .filter(users_goals_association_table.columns.get("user_id") == auth_info.user_id)\
        .filter(Goals.creator_id != auth_info.user_id)\
        .all()

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

    category_ids = post_data.get("category_ids")
    if category_ids:
        post_data.pop("category_ids")

    user_id = post_data.get("user_id")
    if user_id:
        post_data.pop("user_id")

    populate_object(goal_query, post_data)
    goal_query.creator_id = auth_info.user_id

    if category_ids:
        for category_id in category_ids:
            if not validate_uuid4(category_id):
                return jsonify({"message": "invalid category id"}), 400

        categories_query = db.session.query(Categories).filter(Categories.category_id.in_(category_ids)).all()

        for category in categories_query:
            if not category:
                return jsonify({"message": "category not found"}), 404

            if category in goal_query.categories:
                goal_query.categories.pop(goal_query.categories.index(category))

            else:
                goal_query.categories.append(category)

    if user_id:
        if not validate_uuid4(user_id):
            return jsonify({"message": "invalid user id"}), 400

        user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

        if not user_query:
            return jsonify({"message": "user not found"}), 404

        if user_query in goal_query.users:
            goal_query.users.pop(goal_query.users.index(user_query))

        else:
            goal_query.users.append(user_query)

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
