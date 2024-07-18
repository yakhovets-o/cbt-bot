import aiogram.utils.markdown as fmt
from aiogram import types


async def send_currency_page(message: types.Message, currencies: list[dict[str, str]], page_num: int) -> None:
    page_size = 10
    start_idx = (page_num - 1) * page_size
    end_idx = min(start_idx + page_size, len(currencies))
    page_currencies = currencies[start_idx:end_idx]

    currency_list = "\n".join([fmt.text(fmt.hbold(f'{str(*i.keys())} - {str(*i.values())}')) for i in page_currencies])
    await message.answer(text=f'Page {page_num}:\n{currency_list}', parse_mode='HTML')


async def greeting(message: types.Message) -> None:
    your_name = message.from_user.full_name
    time_message_hour = (message.date.time().hour + 3) % 24
    time_of_day = {
        "Доброе утро": tuple(range(4, 12)),
        "Добрый день": tuple(range(12, 17)),
        "Добрый вечер": tuple(range(17, 24)),
        "Доброй ночи": tuple(range(0, 4)),
    }
    text = fmt.text(
        fmt.text(
            fmt.hbold(
                tuple(k for k, v in time_of_day.items() if time_message_hour in v)[0],
                your_name,
            )
        ),
        fmt.text(fmt.hitalic('Это (чат-бот) для отображения актуального курса валют')),
        fmt.text(fmt.hitalic('Для получения списка актуальных курсов валют'), fmt.hbold('/rates')),
        fmt.text(fmt.hitalic('Конвертер  валют'), fmt.hbold('/exchange')),
        fmt.text(fmt.hitalic(f'Пример использования: /exchange USD RUB 10')),
        fmt.text(fmt.hitalic('USD - что меняем')),
        fmt.text(fmt.hitalic('RUB - на что меняем')),
        fmt.text(fmt.hitalic('10 - сумма')),
        sep='\n')

    await message.answer(text=text)