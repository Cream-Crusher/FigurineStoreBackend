# ESBlogBackEnd

Проект интернет магазина фигурок с использованием микросервисов и чистой архитектуры

## Микросервисы

* auth_service: Предсталвение логики login/logout
* mailing_service: Представление логики рассылок
* Проект нахоидтся в разработке и создание новых и обновление текущих сервисов будет добавляться постепенно

### Особенности

* Каждый микросервис является самостоятельным за счет использования микросервисной архитектуры

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

## Инструменты

* Docker
* CI CD
* swagger
