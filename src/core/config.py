import os
from pathlib import Path

from dotenv import load_dotenv

# path = Path(__file__).parent.parent.parent / 'infra/.env'
path = Path(__file__).parent / '.env'
load_dotenv(path)


DEFAULT_TITLE_APP = 'Сервис wallets'
DEFAULT_APP_DESCRIPTION = (
    'Сервис wallets. Позволяет пополнять и списывать средства с виртуальных кошельков.'
    'Так же есть возможность проверять баланс.'
)


class Settings:
    # App
    app_title: str = os.getenv('APP_TITLE', DEFAULT_TITLE_APP)
    app_description: str = os.getenv('APP_DESCRIPTION', DEFAULT_APP_DESCRIPTION)

    # Postgres
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')
    postgres_db: str = os.getenv('POSTGRES_DB')
    db_container_name: str = os.getenv('POSTGRES_CONTAINER_NAME')
    postgres_port: str = os.getenv('POSTGRES_PORT')
    database_url: str = (
        f'postgresql+asyncpg://{postgres_user}:{postgres_password}@'
        f'{db_container_name}:{postgres_port}/{postgres_db}'
    )

    # Redis
    redis_password: str = os.getenv('REDIS_PASSWORD')
    redis_port: str = os.getenv('REDIS_PORT')
    redis_container_name: str = os.getenv('REDIS_CONTAINER_NAME')

    # Wallet
    wallet_uuid: str = os.getenv('WALLET_UUID', '8f4e3a4d-23a4-4b6e-a3d3-8f4e3a4d23a4')
    wallet_balance: float = float(os.getenv('WALLET_BALANCE', 1000.00))

    # Date
    date_format: str = '%a, %d %b %Y %H:%M:%S %z'


settings = Settings()
