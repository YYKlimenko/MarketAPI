### MarketAPI:

Учебный проект, API для интернет-магазина

Используемый стек: Python 3.10, Django 4, Django-rest-framework 3.13, PostgreSQL, Docker, Docker-compose

Установка:
Из рабочего каталога выполните команду: <br>
    `docker-compose up`  <br>
Создайте суперпользователя для администрирования: <br>
    `docker-compose run backend python MarketAPI/manage.py createsuperuser --noinput --email (mail)` <br>

В проекте реализовано: CRUD-операции, аутентификации по сессии, JWT-аутентификация, сериализация данных,
разрешения (permissions), Swagger-документация, unit-тесты, оптимизация sql-запросов, контейнеризация (Docker)
