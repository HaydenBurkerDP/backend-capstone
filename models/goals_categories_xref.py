from db import db

goals_categories_association_table = db.Table(
    "GoalCategoryXref",
    db.Model.metadata,
    db.Column("goal_id", db.ForeignKey("Goals.goal_id"), primary_key=True),
    db.Column("category_id", db.ForeignKey("Categories.category_id"), primary_key=True)
)
