from flask import Blueprint, request

import controllers

goals = Blueprint("goals", __name__)


@goals.route("/goal", methods=["POST"])
def goal_add():
    return controllers.goal_add(request)


@goals.route("/goal/<goal_id>", methods=["GET"])
def goal_get_by_id(goal_id):
    return controllers.goal_get_by_id(request, goal_id)


@goals.route("/goals", methods=["GET"])
def goals_get_all():
    return controllers.goals_get_all(request)


@goals.route("/goals/category/<category_id>", methods=["GET"])
def goals_get_by_category_id(category_id):
    return controllers.goals_get_by_category_id(request, category_id)


@goals.route("/goal/<goal_id>", methods=["PUT"])
def goal_update_by_id(goal_id):
    return controllers.goal_update_by_id(request, goal_id)


@goals.route("/goal/delete/<goal_id>", methods=["DELETE"])
def goal_delete_by_id(goal_id):
    return controllers.goal_delete_by_id(request, goal_id)
