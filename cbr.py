import asyncio
import os
import xml.etree.ElementTree as ET

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.client.session import aiohttp

from constants import COOKIES, HEADERS
from dotenv import find_dotenv, load_dotenv

from redis_helper import redis_db

load_dotenv(find_dotenv())


def save(crb_xml):
    tree = ET.fromstring(crb_xml)
    for currency, price in zip(tree.findall('Valute/CharCode'), tree.findall('Valute/VunitRate')):
        redis_db.set_pair(currency=currency.text, price=price.text)


async def get_cbr_xml():
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=os.getenv('CBR_URL'), cookies=COOKIES, headers=HEADERS)
            cbr_xml = await response.text()
            await asyncio.to_thread(save, cbr_xml)

    except aiohttp.ClientError as ce:
        raise ce
    except Exception as ex:
        raise ex


async def scheduler_jobs():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(get_cbr_xml, 'interval', seconds=60)
    scheduler.add_job(get_cbr_xml, 'cron', hour=8)
    scheduler.start()
