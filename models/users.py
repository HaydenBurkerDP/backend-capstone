from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db
from models.users_goals_xref import users_goals_association_table


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    auth = db.relationship("AuthTokens", back_populates="user", cascade="all,delete")
    goals = db.relationship("Goals", secondary=users_goals_association_table, back_populates="users")
    goal_logs = db.relationship("GoalLogs", back_populates="user", cascade="all,delete")
    created_goals = db.relationship("Goals", back_populates="creator", cascade="all,delete")

    def __init__(self, first_name, last_name, email, password, role, active):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        self.active = active

    def get_new_user():
        return Users("", "", "", "", "user", True)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "first_name", "last_name", "email", "role", "active"]


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
