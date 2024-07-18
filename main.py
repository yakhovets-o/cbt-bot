import asyncio
import os
import aiogram.utils.markdown as fmt

from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from cbr import scheduler_jobs, get_cbr_xml
from redis_helper import redis_db
from tools import send_currency_page, greeting

load_dotenv(find_dotenv())

bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    await greeting(message=message)


@dp.message(Command('rates'))
async def rates(message: types.Message) -> None:
    if not redis_db.pairs():
        await get_cbr_xml()

    exchange_rates = [{pair: redis_db.get_pair(pair)} for pair in redis_db.pairs()]

    current_date = datetime.now().strftime("%d %b %y")

    num_pages = len(exchange_rates) // 10 + 1
    await message.answer(text=fmt.hbold(f'Exchange rates on {current_date} 🕗'))
    for page_num in range(1, num_pages + 1):
        await send_currency_page(message=message, currencies=exchange_rates, page_num=page_num)
        await asyncio.sleep(1.5)
    await message.answer('End')


@dp.message(Command('exchange'))
async def exchange(message: types.Message) -> None:
    text = 'Invalid format . Usage example: /exchange USD RUB 10'
    try:
        _, base_currency, target_currency, amount = message.text.split()

        base_rate = float(redis_db.get_pair(base_currency).replace(',', '.'))
        amount = float(amount)

        if target_currency == 'RUB':
            converted_amount = base_rate * amount
        else:
            converted_amount = base_rate * amount / float(redis_db.get_pair(target_currency).replace(',', '.'))
        await message.answer(text=fmt.hitalic(f'exchange {amount} {base_currency}'
                                              f' to {target_currency} = {converted_amount:.2f} 💵'))
    except ValueError:
        await message.answer(text=text)
    except AttributeError:
        await message.answer(text=text)


async def main():
    await asyncio.gather(bot.delete_webhook(drop_pending_updates=True), dp.start_polling(bot), scheduler_jobs())


if __name__ == '__main__':
    print('Bot started!')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
