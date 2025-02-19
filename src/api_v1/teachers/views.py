from datetime import datetime
from typing import List, Annotated

from fastapi import APIRouter, Depends, Body
from fastapi_cache.decorator import cache

from src.alchemy.db_helper import *
from . import crud
from .schemas import (
    DayScheduleFormatted,
    Teacher,
    DayScheduleTeacher,
    DayScheduleTeacherPydantic, TeacherMonthStats, TeacherMonthStatsRequest,
)

router = APIRouter(tags=["Teachers"])


@router.get("/", response_model=list[Teacher])
@cache(expire=6000)
async def get_groups(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_teachers(session=session)


@router.get("/id/{teacher_id}/", response_model=list[Teacher])
@cache(expire=6000)
async def get_teacher_by_id(
        teacher_id: int = -1,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_teacher_by_id(session=session, teacher_id=teacher_id)


@router.get(
    "/day_schedule/{teacher_id}/{date}/{chat_id}/",
    response_model=DayScheduleTeacherPydantic,
)
@cache(expire=6000)
async def get_teacher_day_schedule_by_date(
        teacher_id: int = -1,
        chat_id: int = -1,
        date: datetime = datetime.now(),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_teacher_day_schedule_by_date(
        session=session, teacher_id=teacher_id, date=date
    )


@router.get(
    "/day_schedule_formatted/{teacher_id}/{date}/{chat_id}/",
    response_model=DayScheduleFormatted,
)
async def get_teacher_day_schedule_by_date_formatted(
        teacher_id: int = -1,
        chat_id: int = -1,
        date: datetime = datetime.now(),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_teacher_day_schedule_by_date_formatted(
        session=session, teacher_id=teacher_id, date=date, chat_id=chat_id
    )


@router.get(
    "/week_schedule/{teacher_id}/{monday_date}/",
    response_model=List[DayScheduleTeacherPydantic],
)
async def get_teacher_week_schedule_by_date(
        teacher_id: int = -1,
        monday_date: datetime = datetime.now(),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_teacher_week_schedule_by_date(
        session=session, teacher_id=teacher_id, monday_date=monday_date
    )


@router.post("/month_stats/", response_model=TeacherMonthStats)
async def get_teacher_month_stats(request: TeacherMonthStatsRequest,
                                  session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_teacher_month_stats(date=request.date, teacher_id=request.teacher_id, session=session)
