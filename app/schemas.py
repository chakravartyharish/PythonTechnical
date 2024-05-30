# from pydantic import BaseModel
# from datetime import date
# from typing import List, Optional
#
# class GroupBase(BaseModel):
#     name: str
#     type: str
#
# class GroupCreate(GroupBase):
#     pass
#
# class Group(GroupBase):
#     id: int
#
#     class Config:
#         orm_mode = True
#
# class SiteBase(BaseModel):
#     name: str
#     installation_date: date
#     max_power_megawatt: float
#     min_power_megawatt: float
#     useful_energy_at_1_megawatt: float
#     efficiency: Optional[float] = None
#
# class SiteCreate(SiteBase):
#     groups: Optional[List[int]] = []
#
# class Site(SiteBase):
#     id: int
#     groups: List[Group] = []
#
#     class Config:
#         orm_mode = True

from pydantic import BaseModel
from datetime import date
from typing import List, Optional

from enum import Enum

class GroupBase(BaseModel):
    name: str
    type: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True


class CountryEnum(str, Enum):
    FR = "FR"
    IT = "IT"


class SiteBase(BaseModel):
    name: str
    installation_date: date
    max_power_megawatt: float
    min_power_megawatt: float
    country: CountryEnum
    useful_energy_at_1_megawatt: float
    efficiency: Optional[float] = None


class SiteCreate(SiteBase):
    groups: Optional[List[int]] = []


class Site(SiteBase):
    id: int
    groups: List[Group] = []

    class Config:
        orm_mode = True
