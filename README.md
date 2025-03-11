REST API на FastAPI, которое позволяет работать с задачами (мини менеджер задач)

Эндпоинты:

- GET /tasks получение списка всех задача (доступны: пагинация, фильтрация по статусу задачи)
- POST /tasks/create создание задачи (задается заголовок и статус)
- PATCH /tasks/update_status/{task_id} обновление статуса задачи


### Стек технологий 
    - Python3.11
    - FastAPI
    - SQLite - СУБД
    - Docker
    - pytest

Тестирование на pytest реализовано для всех эндпоинтов API


#### Запуск приложения

- Копируем код приложения в Вашу директорию

`git clone https://github.com/KIchkinevVladislav/task_manager_test.git`

- Из директории проекта монтируем образ Docker

`docker build -t task_manager_test .`

- Запускаем контейнер

`docker run -d -p 8000:8000 --name app task_manager_test`

При необходимости можете задать свой путь к базе данных при запуске контейнера через переменные окружения: SQLITE_PATH и SQLITE_DB_NAME

- Применяем миграции

`docker exec app alembic upgrade head`

Приложение готово для тестирования:

http://127.0.0.1:8000/docs

#### Запуск тестов

`docker exec app python -m pytest`