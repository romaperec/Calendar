from fastapi import APIRouter, Depends, HTTPException
from schemas import CalendarAddSchema, CalendarUpdateSchema

from database import CalendarEventModel, session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter(prefix="/calendar", tags=["Calendar 📅"])


async def get_session():
    async with session() as conn:
        yield conn


@router.get("/")
async def get_calendar(db: AsyncSession = Depends(get_session)):
    response = await db.execute(select(CalendarEventModel))
    days = response.scalars().all()
    
    if not days:
        return {"message": "DataBase is empty"}
    return days


@router.get("/{day_name}")
async def get_day_by_name(name: str, db: AsyncSession = Depends(get_session)):
    response = await db.execute(select(CalendarEventModel).filter_by(day_name=name))
    day = response.scalars().all()
    
    if not day:
        raise HTTPException(status_code=404, detail="Day not found")
    return day


@router.post("/")
async def create_event(calendar: CalendarAddSchema, db: AsyncSession = Depends(get_session)):
    new_user = CalendarEventModel(day_name=calendar.day_name,
                                  time=calendar.time,
                                  description=calendar.description)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"day_name": new_user.day_name, "time": new_user.time, "description": new_user.description}


@router.patch("/{event_id}")
async def update_event(event_id: int, updated: CalendarUpdateSchema, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CalendarEventModel).where(CalendarEventModel.id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if updated.day_name is not None:
        event.day_name = updated.day_name
    if updated.time is not None:
        event.time = updated.time
    if updated.description is not None:
        event.description = updated.description

    await db.commit()
    await db.refresh(event)

    return {"message": "successfully", "event": event}


@router.delete("/{event_id}")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CalendarEventModel).where(CalendarEventModel.id == event_id))
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found!")

    await db.delete(event)
    await db.commit()

    return {"message": "success", "deleted_note": event}