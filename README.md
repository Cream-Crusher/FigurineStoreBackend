# EZBlogBackEnd

Проект сайта блогов с использованием микросервисов и чистой архитектуры

## Микросервисы

* business_logic_service: Представление логики бизнес процессов
* database_service: Представление логики базы данных
* cache_service: Предсталвение логики кеширования данных
* logger_service: Предсталвение логики логирования и мониторинга процессов

### Особенности

* Каждый микросервис является самостоятельным за счет использования микросервисной архитектуры

## Глобальный стек

* Python
* FastAPI
* SQLAlchemy
* alembic
* asyncio
* aiohttp
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
