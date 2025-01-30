from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy.types import Time
from sqlalchemy import String, Integer, Text

from datetime import time as timeout

engine = create_async_engine("sqlite+aiosqlite:///main.db")
session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    ...


class CalendarEventModel(Base):
    __tablename__ = "calendar_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_name: Mapped[str] = mapped_column(String(11))
    time: Mapped[timeout] = mapped_column(Time)
    description: Mapped[str] = mapped_column(Text)


    @validates("time")
    def validate_time(self, _, value: timeout) -> timeout:
        return timeout(value.hour, value.minute)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)