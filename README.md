# Programming vacancies compare
**Узнаем же где и на каком языке выгоднее программировать!**

## Запуск

Для запуска программы у вас уже должен быть установлен Python.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Установите переменные окружения
- Запустите программу командой `python main.py`

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `main.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следущие переменные:

`SECRET_KEY` - ключ который необходим для функции поиска вакансий на сайте SuperJob. Его можно получить на [официальном сайте Superjob](https://api.superjob.ru/?from_refresh=1#search_vacanices)
## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
