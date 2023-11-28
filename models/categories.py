from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db
from models.goal_logs_categories_xref import goal_logs_categories_association_table
from models.goals_categories_xref import goals_categories_association_table


class Categories(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), nullable=False)

    goals = db.relationship("Goals", secondary=goals_categories_association_table, back_populates="categories")
    goal_logs = db.relationship("GoalLogs", secondary=goal_logs_categories_association_table, back_populates="categories")

    def __init__(self, name, active):
        self.name = name
        self.active = active

    def get_new_category():
        return Categories("", True)


class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ["category_id", "name", "active"]


category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)
