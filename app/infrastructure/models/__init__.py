# from enum import Enum
# from sqlalchemy import Column, Integer, String, Float, Date, Enum as SqlEnum, ForeignKey, Table
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# # Association table for many-to-many relationship between sites and groups
# site_group_association = Table(
#     'site_group_association', Base.metadata,
#     Column('site_id', Integer, ForeignKey('sites.id')),
#     Column('group_id', Integer, ForeignKey('groups.id'))
# )
#
# class Site(Base):
#     __tablename__ = 'sites'
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     installation_date = Column(Date)
#     max_power_megawatt = Column(Float)
#     min_power_megawatt = Column(Float)
#     useful_energy_at_1_megawatt = Column(Float, nullable=True)
#     efficiency = Column(Float, nullable=True)
#     groups = relationship("Group", secondary=site_group_association, back_populates="sites")
#
# class GroupType(Enum):
#     GROUP1 = "group1"
#     GROUP2 = "group2"
#     GROUP3 = "group3"
#
# class Group(Base):
#     __tablename__ = 'groups'
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     type = Column(SqlEnum(GroupType))
#     parent_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
#     sites = relationship("Site", secondary=site_group_association, back_populates="groups")
#     subgroups = relationship("Group", backref="parent", remote_side=[id])
#
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Ensure to import all your models here so that they are registered with the Base metadata
from .group import Group  # Import the Group model
from .site import Site  # Import the Site model
