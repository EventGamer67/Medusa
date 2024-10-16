from typing import Any

import docker
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


def get_containers():
    client = docker.from_env()  # Используем Docker SDK для Python
    containers = client.containers.list(all=True)  # Получаем список всех контейнеров
    container_info = []

    for container in containers:
        # Получаем атрибуты контейнера (включает информацию о состоянии)
        container_attrs = container.attrs
        state = container_attrs["State"]

        # Время завершения контейнера (если остановлен)
        finished_at = (
            state["FinishedAt"]
            if state["FinishedAt"] != "0001-01-01T00:00:00Z"
            else None
        )

        container_info.append(
            {
                "name": container.name,
                "status": container.status,
                "image": container.image.tags,
                "started_at": state["StartedAt"],  # Время запуска контейнера
                "finished_at": finished_at,  # Время завершения работы (если остановлен)
            }
        )

    return {"containers": container_info}
