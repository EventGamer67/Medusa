from typing import Any

from celery.result import AsyncResult
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.alchemy import database
from src.api_v1.parser.schemas import ParseZamenaRequest
from src.parser import tasks


async def parse_zamena(request: ParseZamenaRequest):
    url = request.url
    date = request.date
    task: AsyncResult = tasks.parse_zamena.delay(url=url, date=date)
    return task.get()


async def get_latest_zamena_link():
    task: AsyncResult = tasks.get_latest_zamena_link.delay()
    return task.get()


async def check_new() -> dict[str, Any]:
    task: AsyncResult = tasks.check_new.delay()
    return task.get()


async def get_founded_links(session: AsyncSession):
    links = list(
        (await session.execute(select(database.AlreadyFoundsLinks))).scalars().all()
    )
    return [link.link for link in links]
