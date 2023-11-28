from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db
from models.users_goals_xref import users_goals_association_table
from models.goals_categories_xref import goals_categories_association_table


class Goals(db.Model):
    __tablename__ = "Goals"

    goal_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)

    users = db.relationship("Users", secondary=users_goals_association_table, back_populates="goals")
    creator = db.relationship("Users", back_populates="created_goals")
    categories = db.relationship("Categories", secondary=goals_categories_association_table, back_populates="goals")
    goal_logs = db.relationship("GoalLogs", back_populates="goal")

    def __init__(self, name, description, creator_id):
        self.name = name
        self.description = description
        self.creator_id = creator_id

    def get_new_goal():
        return Goals("", "", "")


class GoalsSchema(ma.Schema):
    class Meta:
        fields = ["goal_id", "name", "description", "creator", "categories"]

    creator = ma.fields.Nested("UsersSchema")
    categories = ma.fields.Nested("CategoriesSchema", many=True)


goal_schema = GoalsSchema()
goals_schema = GoalsSchema(many=True)
