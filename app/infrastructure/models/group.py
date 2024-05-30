
# group.py
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.models.db import Base
from enum import Enum as PyEnum

class GroupType(PyEnum):
    GROUP1 = "group1"
    GROUP2 = "group2"
    GROUP3 = "group3"

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(GroupType), index=True)
    parent_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

    sites = relationship('Site', secondary='site_group_association', back_populates='groups')
    subgroups = relationship("Group", backref="parent", remote_side=[id])
