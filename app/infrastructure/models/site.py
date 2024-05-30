# site.py
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.infrastructure.models.db import Base

# Association table for many-to-many relationship between sites and groups
site_group_association = Table(
    'site_group_association',
    Base.metadata,
    Column('site_id', Integer, ForeignKey('sites.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

class Site(Base):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    installation_date = Column(Date)
    max_power_megawatt = Column(Float)
    min_power_megawatt = Column(Float)
    useful_energy_at_1_megawatt = Column(Float)
    efficiency = Column(Float, nullable=True)

    groups = relationship(
        "Group",
        secondary=site_group_association,
        back_populates="sites"
    )