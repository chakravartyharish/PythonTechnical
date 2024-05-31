from pydantic import BaseModel
from datetime import date
from typing import List, Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .schemas import Site

# Enums
class CountryEnum(str, Enum):
    FR = "FR"
    IT = "IT"

class GroupType(str, Enum):
    GROUP1 = "GROUP1"
    GROUP2 = "GROUP2"
    GROUP3 = "GROUP3"

# Base Models
class GroupBase(BaseModel):
    name: str
    type: GroupType

class SiteBase(BaseModel):
    name: str
    installation_date: date
    max_power_megawatt: float
    min_power_megawatt: float
    country: CountryEnum

# Create Models
class GroupCreate(GroupBase):
    id: int

class SiteCreate(SiteBase):
    useful_energy_at_1_megawatt: Optional[float] = None
    efficiency: Optional[float] = None
    groups: Optional[List[int]] = []

# Response Models with ORM mode enabled
class GroupSchema(BaseModel):
    id: int
    name: str
    type: GroupType

    class Config:
        orm_mode = True

class SiteSchema(BaseModel):
    id: int
    name: str
    installation_date: date
    max_power_megawatt: float
    min_power_megawatt: float
    useful_energy_at_1_megawatt: float
    efficiency: float
    country: CountryEnum
    groups: List[GroupSchema] = []

    class Config:
        orm_mode = True

# ORM Models with forward references
class Group(GroupBase):
    id: int
    sites: List["Site"] = []

    class Config:
        orm_mode = True

class Site(SiteBase):
    id: int
    useful_energy_at_1_megawatt: Optional[float] = None
    efficiency: Optional[float] = None
    groups: List["Group"] = []

    class Config:
        orm_mode = True

# Handle forward references
Group.update_forward_refs()
Site.update_forward_refs()
