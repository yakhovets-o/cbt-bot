# Bot cbt

#### 🛠️ Функциональные Возможнотси 

1. **Сервис получения курсов валют**:
    - Ежедневно получает XML файл с курсами валют с сайта Центрального банка России (ЦБ РФ) по [этой ссылке](https://cbr.ru/scripts/XML_daily.asp).
    - Обновляет данные в Redis, для каждого курса валюты свой ключ.

2. **Сервис бота**:
    - Отвечает на команду `/exchange`, например: `/exchange USD RUB 10` и отображает стоимость 10 долларов в рублях.
    - Отвечает на команду `/rates`, отправляя пользователю актуальные курсы валют.
### 🚀 Запуск 
- `docker-compose up -d`


