from db import db

users_goals_association_table = db.Table(
    "UserGoalXref",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("Users.user_id"), primary_key=True),
    db.Column("goal_id", db.ForeignKey("Goals.goal_id"), primary_key=True)
)
