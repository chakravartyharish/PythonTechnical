from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.models.db import Base
import enum

class GroupType(enum.Enum):
    GROUP1 = "GROUP1"
    GROUP2 = "GROUP2"
    GROUP3 = "GROUP3"

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    parent_id = Column(Integer, ForeignKey('groups.id'))
    parent = relationship("Group", remote_side=[id], back_populates="children")
    children = relationship("Group", back_populates="parent")
    sites = relationship("Site", secondary="site_group_association", back_populates="groups")
