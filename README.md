# API для работы с кошельками

Сервис wallets. Позволяет пополнять и списывать средства с виртуальных кошельков.
Так же есть возможность проверять баланс.

С помощью redis кешируются ответы после изменений в балансе кошелька. При GET запросе баланса 
кошелька, данные возвращаются из кэша, если он есть, иначе из базы данных.

Тесты запускаются автоматически при запуске контейнера.

<details><summary>Задание</summary>
<br>

Напишите приложение, которое по REST принимает запрос вида  
POST `api/v1/wallets/<WALLET_UUID>/operation`

```json
    {
        operationType: DEPOSIT or WITHDRAW,
        amount: 1000
    }
```
после выполнять логику по изменению счета в базе данных
также есть возможность получить баланс кошелька

GET `api/v1/wallets/{WALLET_UUID}`

стек:  
FastAPI / Flask / Django  
Postgresql 

Должны быть написаны миграции для базы данных с помощью liquibase (по желанию)

Обратите особое внимание проблемам при работе в конкурентной среде (1000 RPS по одному кошельку).

Ни один запрос не должен быть не обработан (50Х error)

Предусмотрите соблюдение формата ответа для заведомо неверных запросов, когда кошелька не существует, не валидный json, или недостаточно средств.

приложение должно запускаться в докер контейнере, база данных тоже, вся система должна подниматься с помощью docker-compose

предусмотрите возможность настраивать различные параметры приложения и базы данных без пересборки контейнеров.

эндпоинты должны быть покрыты тестами.

</details>

## Запуск проекта

- Клонируйте репозиторий
```bash
git clone git@github.com:AndreyKilanov/wallet_test_task.git
```

- Создайте и заполните `.env` по пути `./infra`
- Передайте uuid4 кошелька и его начальный баланс. После запуска проекта кошелек будет создан в БД

```bash
# Postgres
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres_db
POSTGRES_PORT=5432
POSTGRES_CONTAINER_NAME=postgres

# Redis
REDIS_PASSWORD=password
REDIS_PORT=6379
REDIS_CONTAINER_NAME=redis

# Wallet UUID V4
WALLET_UUID=84642644-da1b-462b-8be2-b2bcea2c9db6
BALANCE=1000
```


- Запустите контейнера из `./infra` командой:
```bash
docker-compose up -d --build
```
- После запуска проекта Swagger будет доступен по [адресу](http://127.0.0.1:8000/docs)

## Стек

1. [x] fastapi[standard] 0.115.5
2. [x] SQLAlchemy 2.0.36
3. [x] alembic 1.14.0
4. [x] asyncpg 0.30.0
5. [x] redis 5.2.0
6. [x] pytest 8.3.3


## Контакты
[![](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/AndyFebruary)