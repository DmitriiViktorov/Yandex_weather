# Weather Forecast Excel Reporter

## Описание проекта

Программа получает прогноз погоды на 7 дней для указанного города с сайта Яндекс.Погода и формирует Excel-файл с прогнозом.  
Также ведется логирование запросов и результатов работы в SQLite (город, координаты, дата/время, успешность или ошибка).

---

## Установка и запуск

1. Склонировать проект и перейти в его папку:

```bash
git clone https://github.com/DmitriiViktorov/Yandex_weather.git
```

2. Создать виртуальное окружение и активировать его:

```bash
python -m venv .venv
# Linux / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt 
```

4. Запустить FastAPI сервер:

```bash
uvicorn app.main:app --reload
```

Сервер будет доступен по адресу http://127.0.0.1:8000. Интерфейс позволяет выбрать город и скачать Excel-отчет.


## Структура проекта

- app/main.py — запуск FastAPI.
- app/models.py — модели для логирования.

- app/services/db.py — работа с SQLite.
- app/services/parser.py — парсер Яндекс.Погоды.
- app/services/weather.py — обработка и анализ данных.
- app/services/excel.py — формирование Excel-файлов.

## Примечания

Для корректной работы требуется подключение к интернету.

SQLite база создается автоматически при первом запуске.

