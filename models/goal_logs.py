from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db
from models.goal_logs_categories_xref import goal_logs_categories_association_table


class GoalLogs(db.Model):
    __tablename__ = "GoalLogs"

    goal_log_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    goal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Goals.goal_id"))
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    completion_date = db.Column(db.DateTime())

    categories = db.relationship("Categories", secondary=goal_logs_categories_association_table, back_populates="goal_logs")
    user = db.relationship("Users", back_populates="goal_logs")
    goal = db.relationship("Goals", back_populates="goal_logs")

    def __init__(self, user_id, goal_id, name, description, start_date, end_date, completion_date):
        self.user_id = user_id
        self.goal_id = goal_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.completion_date = completion_date

    def get_new_goal_log():
        return GoalLogs(None, None, "", "", None, None, None)


class GoalLogsSchema(ma.Schema):
    class Meta:
        fields = ["goal_log_id", "user", "goal_id", "name", "description", "start_date", "end_date", "completion_date", "categories"]

    user = ma.fields.Nested("UsersSchema")
    categories = ma.fields.Nested("CategoriesSchema", many=True)


goal_log_schema = GoalLogsSchema()
goal_logs_schema = GoalLogsSchema(many=True)
