from fastapi import APIRouter, Depends
from schemas import CalendarAddSchema

from database import CalendarEventModel, session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter(prefix="/calendar", tags=["Calendar"])


async def get_session():
    async with session() as conn:
        yield conn


@router.get("/")
async def get_calendar(db: AsyncSession = Depends(get_session)):
    response = await db.execute(select(CalendarEventModel))
    days = response.scalars().all()
    return days


@router.get("/{day_name}")
async def get_day_by_name(name: str, db: AsyncSession = Depends(get_session)):
    response = await db.execute(select(CalendarEventModel).filter_by(day_name=name))
    day = response.scalars().all()
    return day


@router.post("/")
async def create_day(calendar: CalendarAddSchema, db: AsyncSession = Depends(get_session)):
    new_user = CalendarEventModel(day_name=calendar.day_name,
                                  time=calendar.time,
                                  description=calendar.description)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"day_name": new_user.day_name, "time": new_user.time, "description": new_user.description}


@router.patch("/{event_id}")
async def update_note(event_id: int, updated: CalendarAddSchema, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CalendarEventModel).where(CalendarEventModel.id == event_id))
    event = result.scalar_one_or_none()

    event.day_name = updated.day_name
    event.time = updated.time
    event.description = updated.description

    await db.commit()
    await db.refresh(event)
    return {"message": "successfully", "event": event}


@router.delete("/{event_id}")
async def delete_note(event_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CalendarEventModel).where(CalendarEventModel.id == event_id))
    note = result.scalar_one_or_none()
    await db.delete(note)
    await db.commit()
    return {"message": "success", "deleted_note": note}