from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from app.infrastructure.models.db import Base

# Association table for many-to-many relationship between sites and groups
site_group_association = Table(
    "site_group_association",
    Base.metadata,
    Column("site_id", Integer, ForeignKey("sites.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    installation_date = Column(Date, nullable=False)
    max_power_megawatt = Column(Float, nullable=False)
    min_power_megawatt = Column(Float, nullable=False)
    useful_energy_at_1_megawatt = Column(Float, nullable=True)
    efficiency = Column(Float, nullable=True)
    country = Column(Enum("FR", "IT", name="country_enum"), nullable=False)

    groups = relationship(
        "Group", secondary=site_group_association, back_populates="sites"
    )
