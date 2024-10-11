# import asyncio
# import datetime
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# from typing import List
# from aiogram.fsm.storage import redis
#
# # from celery import signature
# # from celery.result import AsyncResult
#
# from bot_worker import parse_zamenas
# from bot_worker.bot import admins
# from broker import rabbitmq_channel
#
# # from broker import sup, parser_celery_app
# from parser_secrets import (
#     DEBUG_CHANNEL,
#     REDIS_HOST_URL,
#     REDIS_PORT,
#     REDIS_PASSWORD,
#     REDIS_USERNAME,
#     SCHEDULE_URL,
# )
# from src.code.core.schedule_parser import (
#     getLastZamenaLink,
#     getAllMonthTables,
#     getAllTablesLinks,
# )
# from src.code.models.parsed_date_model import ParsedDate
# from src.code.models.zamena_table_model import ZamTable
#
#
# # Функция для отправки сообщений в очередь
# def send_message_to_rabbitmq(message: str) -> None:
#     print(rabbitmq_channel)
#     if rabbitmq_channel is None:
#         print("RabbitMQ channel is not initialized")
#         raise Exception("RabbitMQ channel is not initialized")
#
#     rabbitmq_channel.basic_publish(exchange="", routing_key="parser", body=message)
#     print(f" [x] Sent '{message}' to queue 'parser'")
import datetime
from typing import List
from urllib.request import urlopen

from bs4 import BeautifulSoup

from my_secrets import SCHEDULE_URL
from src.parser.core import getLastZamenaLink, getAllMonthTables, getAllTablesLinks
from src.parser.models.parsed_date_model import ParsedDate
from src.parser.models.zamena_table_model import ZamTable
from src.parser.parsers import parse_zamenas
from src.parser.supabase import SupaBaseWorker

sup = SupaBaseWorker()
# async def send_task(celery_app, task_name: str, args: list = list) -> AsyncResult:
#     max_retries = 5
#     retries = 0
#     while retries < max_retries:
#         task = celery_app.send_task(task_name, args=args)
#         task_id = task.id
#         result = AsyncResult(task_id)
#
#         while not result.ready():
#             await asyncio.sleep(1)
#
#         if result.successful():
#             return result
#         elif result.failed():
#             retries += 1
#             if retries == max_retries:
#                 raise Exception("Достигнут лимит попыток. Попробуйте позже.")
#         raise Exception("Хз что произошло")


def parse_zamena(url: str, date: datetime.datetime):
    try:
        parse_zamenas(url=url, date_=date)
        return {"res": "ok"}
    except Exception as e:
        return {"res": f"{str(e)}"}


def get_latest_zamena_link():
    try:
        html = urlopen("https://www.uksivt.ru/zameny").read()
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        link, date = getLastZamenaLink(soup=soup)
        return {"date": date, "link": link}
    except Exception as e:
        return {"message": "failed", "reason": str(e)}


def check_new():

    # r = redis.Redis(
    #     host=REDIS_HOST_URL,
    #     port=REDIS_PORT,
    #     decode_responses=True,
    #     password=REDIS_PASSWORD,
    #     username=REDIS_USERNAME,
    # )

    # res = await r.lrange("alreadyFound", 0, -1)
    # return res
    html = urlopen(SCHEDULE_URL).read()

    soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
    tables: List[ZamTable] = getAllMonthTables(soup=soup)
    site_links = getAllTablesLinks(tables)
    database_links: List[ParsedDate] = sup.get_zamena_file_links()
    already_found_links = []
    # await on_check(bot=bot)
    if not site_links.__eq__(database_links):
        # alreadyFound = await r.lrange("alreadyFound", 0, -1)
        new_links = list(
            set(site_links)
            - set([x.link for x in database_links])
            - set(already_found_links)
        )
        new_links.reverse()
        print(new_links)
        if len(new_links) < 1:
            return {"res": "no_new_links"}
        return {"res": "found_new", "links": new_links}
        # for i in link
    #         for i in tables[0].zamenas:
    #             if (i.date > datetime.date.today()):
    #                 hash = get_remote_file_hash(i.link)
    #                 try:
    #                     oldhash = [x for x in databaseLinks if x.link == i.link][0].hash
    #                     if hash != oldhash:
    #                         await bot.send_message(chat_id=admins[0], text=f'Обнаружен перезалив на {i.link} {i.date}')
    #                         extension = get_file_extension(i.link)
    #                         filename = i.link.split('/')[-1].split('.')[0]
    #                         downloadFile(link=i.link, filename=f"{filename}.{extension}")
    #                         if extension == 'pdf':
    #                             screenshot_paths = await create_pdf_screenshots(filename)
    #                         if extension == 'docx':
    #                             convert(f"{filename}.{extension}")
    #                             screenshot_paths = await create_pdf_screenshots(filename)
    #                         media_group = MediaGroupBuilder(
    #                             caption=f"Перезалив замен на <a href='{i.link}'>{i.date}</a>  ")
    #
    #                         for j in screenshot_paths:
    #                             image = FSInputFile(j)
    #                             media_group.add_photo(image)
    #                         try:
    #                             await bot.send_media_group(-1002035415883, media=media_group.build())
    #                             send_message_to_topic('Перезалив замен',
    #                                                   f'Обнаружен перезалив замен на {i.date}', sup=sup)
    #                         except Exception as error:
    #                             await bot.send_message(chat_id=admins[0], text=str(error))
    #                         subs = await r.lrange("subs", 0, -1)
    #                         for j in subs:
    #                             try:
    #                                 await bot.send_media_group(j, media=media_group.build())
    #                             except Exception as error:
    #                                 try:
    #                                     await bot.send_message(chat_id=admins[0], text=str(error))
    #                                 except:
    #                                     continue
    #                         cleanup_temp_files(screenshot_paths)
    #                         os.remove(f"{filename}.pdf")
    #                         datess = datetime.datetime(year=i.date.year, month=i.date.month, day=i.date.day)
    #                         sup.table('Zamenas').delete().eq('date', datess).execute()
    #                         sup.table('ZamenasFull').delete().eq('date', datess).execute()
    #                         res = sup.table('ZamenaFileLinks').update({'hash': hash}).eq('link', i.link).execute()
    #                         await bot.send_message(chat_id=admins[0], text=f'Обновлен хеш {res}')
    #                         parse_zamenas(url=i.link, date_=datess)
    #                         await bot.send_message(chat_id=admins[0], text='parsed')
    #                 except Exception as error:
    #                     print(error)
    #                     await bot.send_message(chat_id=admins[0], text=str(error.__str__()))
    #         return
    #     for link in new:
    #         zam = [x for x in tables if x.links.__contains__(link)][0]
    #         zamm = [x for x in zam.zamenas if x.link == link][0]
    #         try:
    #             await r.lpush("alreadyFound", str(zamm.link))
    #             if (link.__contains__('google.com') or link.__contains__('yadi.sk')):
    #                 continue
    #             extension = get_file_extension(zamm.link)
    #             filename = zamm.link.split('/')[-1].split('.')[0]
    #             downloadFile(link=zamm.link, filename=f"{filename}.{extension}")
    #             if extension == 'pdf':
    #                 screenshot_paths = await create_pdf_screenshots(filename)
    #             if extension == 'docx':
    #                 convert(f"{filename}.{extension}")
    #                 screenshot_paths = await create_pdf_screenshots(filename)
    #             media_group = MediaGroupBuilder(caption=f"Новые замены на <a href='{zamm.link}'>{zamm.date}</a>  ")
    #             for i in screenshot_paths:
    #                 image = FSInputFile(i)
    #                 media_group.add_photo(image)
    #             try:
    #                 # await bot.send_media_group(chat_id=admins[0], media=media_group.build())
    #                 await bot.send_media_group(-1002035415883, media=media_group.build())
    #                 send_message_to_topic('Новые замены', f'Новые замены на {zamm.date}', sup=sup)
    #             except Exception as error:
    #                 await bot.send_message(chat_id=admins[0], text=str(error))
    #             subs = await r.lrange("subs", 0, -1)
    #             for i in subs:
    #                 try:
    #                     await bot.send_media_group(i, media=media_group.build())
    #                 except Exception as error:
    #                     try:
    #                         await bot.send_message(chat_id=admins[0], text=str(error))
    #                     except:
    #                         continue
    #             cleanup_temp_files(screenshot_paths)
    #             os.remove(f"{filename}.pdf")
    #             datess = datetime.date(zamm.date.year, zamm.date.month, zamm.date.day)
    #             sup.table('Zamenas').delete().eq('date', datess).execute()
    #             sup.table('ZamenasFull').delete().eq('date', datess).execute()
    #             sup.table('ZamenaFileLinks').delete().eq('date', datess).execute()
    #             parse_zamenas(url=zamm.link, date_=datess)
    #             await bot.send_message(chat_id=admins[0], text='parsed')
    #         except Exception as error:
    #             await bot.send_message(chat_id=admins[0], text=f'{str(error)}\n{str(error.__traceback__)}')
    return {"res": "ok"}
