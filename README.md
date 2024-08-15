# Figurine Store

Проект интернет магазина фигурок с использованием микросервисов и чистой архитектуры

![изображение](https://github.com/user-attachments/assets/0a0d9404-555d-4936-abb7-67402dd37700)

## Микросервисы

* auth_service: Предсталвение логики login/logout
* mailing_service: Сервис рассылок сообщений
* catalog_service: Сервис каталога товаров
* basket_service: Сервис корзины пользователя
* ordering_service: Сервис заказов пользователя

## Глобальный стек

* Python
* FastAPI
* SQLAlchemy
* alembic
* asyncio
* aiohttp
* httpx
* RabbitMQ | Aio Pika
* Redis | redis
* pyotp
* unittest
* environs

## Базы данных

* PostgreSQL + asyncpg
* Redis
* MongoDB

## Деплой

* Docker
