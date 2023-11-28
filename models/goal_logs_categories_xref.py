from db import db

goal_logs_categories_association_table = db.Table(
    "GoalLogCategoryXref",
    db.Model.metadata,
    db.Column("goal_log_id", db.ForeignKey("GoalLogs.goal_log_id"), primary_key=True),
    db.Column("category_id", db.ForeignKey("Categories.category_id"), primary_key=True)
)
