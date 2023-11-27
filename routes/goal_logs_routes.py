from flask import Blueprint, request

import controllers

goal_logs = Blueprint("goal logs", __name__)


@goal_logs.route("/goal-log", methods=["POST"])
def goal_log_add():
    return controllers.goal_log_add(request)


@goal_logs.route("/goal-log/<goal_log_id>", methods=["GET"])
def goal_log_get_by_id(goal_log_id):
    return controllers.goal_log_get_by_id(request, goal_log_id)


@goal_logs.route("/goal-logs", methods=["GET"])
def goal_logs_get_all():
    return controllers.goal_logs_get_all(request)


@goal_logs.route("/goal-log/<goal_log_id>", methods=["PUT"])
def goal_log_update_by_id(goal_log_id):
    return controllers.goal_log_update_by_id(request, goal_log_id)


@goal_logs.route("/goal-log/delete/<goal_log_id>", methods=["DELETE"])
def goal_log_delete_by_id(goal_log_id):
    return controllers.goal_log_delete_by_id(request, goal_log_id)
