# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from app.infrastructure.models.db import get_session
from app.infrastructure.models.group import Group, GroupType
from app.infrastructure.models.site import Site
from app.schemas import Site as SiteSchema, SiteCreate, Group as GroupSchema, GroupCreate
from typing import List
import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.infrastructure.models.db import get_session
from typing import List, AsyncGenerator
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.models.db import get_session, Base, engine
from app.infrastructure.models import Site, Group
from app.schemas import SiteCreate, Site, GroupCreate, Group
from datetime import date, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()


# Create the database tables on app startup
@app.on_event("startup")
async def startup():
    logging.info("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# @app.post("/sites/", response_model=SiteSchema)
# async def create_site(site: SiteCreate, db: AsyncSession = Depends(get_session)):
#     logger.debug("create_site called with site: %s", site)
#     try:
#         async with db.begin():
#             if site.efficiency is None:  # Assuming French sites don't have efficiency
#                 result = await db.execute(
#                     select(Site)
#                     .where(Site.installation_date == site.installation_date)
#                     .options(joinedload(Site.groups))
#                 )
#                 existing_site = result.scalars().first()
#                 logger.debug("Existing site: %s", existing_site)
#                 if existing_site:
#                     raise HTTPException(status_code=400, detail="A French site is already installed on this date")
#             else:  # Assuming Italian sites have efficiency
#                 if site.installation_date.weekday() not in (5, 6):  # Saturday and Sunday
#                     raise HTTPException(status_code=400, detail="Italian sites must be installed on weekends")
#
#             db_site = Site(
#                 name=site.name,
#                 installation_date=site.installation_date,
#                 max_power_megawatt=site.max_power_megawatt,
#                 min_power_megawatt=site.min_power_megawatt,
#                 useful_energy_at_1_megawatt=site.useful_energy_at_1_megawatt,
#                 efficiency=site.efficiency
#             )
#             db.add(db_site)
#
#             # Handle groups
#             if site.groups:
#                 for group_id in site.groups:
#                     result = await db.execute(select(Group).where(Group.id == group_id))
#                     group = result.scalars().first()
#                     logger.debug("Group: %s", group)
#                     if group and group.type == GroupType.GROUP3:
#                         raise HTTPException(status_code=400, detail="A site cannot be associated with a group of type 'group3'")
#                     db_site.groups.append(group)
#
#         await db.commit()
#         await db.refresh(db_site)
#         logger.debug("Created site: %s", db_site)
#         return db_site
#
#     except IntegrityError as e:
#         await db.rollback()
#         logger.error("IntegrityError: %s", e)
#         raise HTTPException(status_code=400, detail=str(e))
@app.post("/sites/", response_model=Site, status_code=201)
async def create_site(site: SiteCreate, db: AsyncSession = Depends(get_session)):
    # Business Logic Checks (Async)
    if site.country == "FR":
        yesterday = date.today() - timedelta(days=1)
        result = await db.execute(
            select(Site).filter(
                Site.country == "FR", Site.installation_date >= yesterday
            )
        )
        if result.scalars().all():  # Check if any results were found
            raise HTTPException(
                status_code=400,
                detail="Only one French site can be installed per day.",
            )

    if site.country == "IT" and date.today().weekday() not in (5, 6):
        raise HTTPException(
            status_code=400, detail="Italian sites can only be installed on weekends."
        )

    # Check for existing site with the same name
    existing_site = await db.execute(
        select(Site).filter(Site.name == site.name)
    )
    if existing_site.scalars().first():
        raise HTTPException(status_code=400, detail="Site name already exists")

    if any(group.type == "group3" for group in site.groups):
        raise HTTPException(
            status_code=400, detail="Sites cannot be associated with group type 'group3'."
        )

    # Create Site object
    db_site = Site(**site.dict())

    # Add groups to the site
    for group_data in site.groups:
        group = await db.execute(
            select(Group).filter(Group.name == group_data.name)
        )
        group = group.scalars().first()
        if group is None:
            group = Group(name=group_data.name, type=group_data.type)
            db.add(group)
        db_site.groups.append(group)

    db.add(db_site)
    await db.commit()
    await db.refresh(db_site)
    return db_site
@app.get("/sites/{site_id}", response_model=SiteSchema)
async def read_site(site_id: int, db: AsyncSession = Depends(get_session)):
    logger.debug("read_site called with site_id: %d", site_id)
    result = await db.execute(
        select(Site)
        .options(joinedload(Site.groups))
        .where(Site.id == site_id)
    )
    db_site = result.scalars().first()
    logger.debug("Read site: %s", db_site)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site

@app.patch("/sites/{site_id}", response_model=SiteSchema)
async def update_site(site_id: int, site: SiteCreate, db: AsyncSession = Depends(get_session)):
    logger.debug("update_site called with site_id: %d and site: %s", site_id, site)
    try:
        async with db.begin():
            result = await db.execute(
                select(Site)
                .where(Site.id == site_id)
                .options(joinedload(Site.groups))
            )
            db_site = result.scalars().first()
            if db_site is None:
                raise HTTPException(status_code=404, detail="Site not found")

            for key, value in site.dict().items():
                setattr(db_site, key, value)

        await db.commit()
        await db.refresh(db_site)
        logger.debug("Updated site: %s", db_site)
        return db_site

    except IntegrityError as e:
        await db.rollback()
        logger.error("IntegrityError: %s", e)
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/sites/{site_id}")
async def delete_site(site_id: int, db: AsyncSession = Depends(get_session)):
    logger.debug("delete_site called with site_id: %d", site_id)
    try:
        async with db.begin():
            result = await db.execute(
                select(Site)
                .where(Site.id == site_id)
                .options(joinedload(Site.groups))
            )
            db_site = result.scalars().first()
            if db_site is None:
                raise HTTPException(status_code=404, detail="Site not found")

            await db.delete(db_site)
        await db.commit()
        logger.debug("Deleted site: %d", site_id)
        return {"message": "Site deleted successfully"}

    except IntegrityError as e:
        await db.rollback()
        logger.error("IntegrityError: %s", e)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/groups/", response_model=GroupSchema)
async def create_group(group: GroupCreate, db: AsyncSession = Depends(get_session)):
    logger.debug("create_group called with group: %s", group)
    try:
        async with db.begin():
            db_group = Group(**group.dict())
            db.add(db_group)
        await db.commit()
        await db.refresh(db_group)
        logger.debug("Created group: %s", db_group)
        return db_group

    except IntegrityError as e:
        await db.rollback()
        logger.error("IntegrityError: %s", e)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/groups/{group_id}", response_model=GroupSchema)
async def read_group(group_id: int, db: AsyncSession = Depends(get_session)):
    logger.debug("read_group called with group_id: %d", group_id)
    result = await db.execute(select(Group).where(Group.id == group_id))
    db_group = result.scalars().first()
    logger.debug("Read group: %s", db_group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@app.patch("/groups/{group_id}", response_model=GroupSchema)
async def update_group(group_id: int, group: GroupCreate, db: AsyncSession = Depends(get_session)):
    logger.debug("update_group called with group_id: %d and group: %s", group_id, group)
    try:
        async with db.begin():
            result = await db.execute(select(Group).where(Group.id == group_id))
            db_group = result.scalars().first()
            if db_group is None:
                raise HTTPException(status_code=404, detail="Group not found")

            for key, value in group.dict().items():
                setattr(db_group, key, value)

        await db.commit()
        await db.refresh(db_group)
        logger.debug("Updated group: %s", db_group)
        return db_group

    except IntegrityError as e:
        await db.rollback()
        logger.error("IntegrityError: %s", e)
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/groups/{group_id}")
async def delete_group(group_id: int, db: AsyncSession = Depends(get_session)):
    logger.debug("delete_group called with group_id: %d", group_id)
    try:
        async with db.begin():
            result = await db.execute(select(Group).where(Group.id == group_id))
            db_group = result.scalars().first()
            if db_group is None:
                raise HTTPException(status_code=404, detail="Group not found")

            await db.delete(db_group)
        await db.commit()
        logger.debug("Deleted group: %d", group_id)
        return {"message": "Group deleted successfully"}

    except IntegrityError as e:
        await db.rollback()
        logger.error("IntegrityError: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
