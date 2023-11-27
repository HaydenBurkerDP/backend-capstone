from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db


class Goals(db.Model):
    __tablename__ = "Goals"

    goal_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)

    def __init__(self, name, description, creator_id):
        self.name = name
        self.description = description
        self.creator_id = creator_id

    def get_new_goal():
        return Goals("", "", "")


class GoalsSchema(ma.Schema):
    class Meta:
        fields = ["goal_id", "name", "description", "creator_id"]


goal_schema = GoalsSchema()
goals_schema = GoalsSchema(many=True)
