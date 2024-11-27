import json
import logging

import redis

from core.config import settings
from models import Wallet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


redis_cache = redis.Redis(
    host=settings.redis_container_name,
    port=settings.redis_port,
    password=settings.redis_password,
    encoding='utf-8',
    db=0
)


def ping_redis_cache():
    """
    Проверяет доступность Redis.
    """
    try:
        info = redis_cache.info()
        logger.info(f"Redis version: {info['redis_version']}")
        response = redis_cache.ping()

        if response:
            logger.info("Redis connected!")
        else:
            logger.warning("Redis not connected!")

    except redis.ConnectionError as e:
        logger.error(f"Error: {e}")


def add_data_to_cache(wallet: Wallet):
    """
    Добавляет данные кошелька в кеш Redis.

    :param wallet: Объект кошелька, который нужно сохранить в кеш
    """
    try:
        redis_cache.set(
            wallet.uuid,
            json.dumps({'id': wallet.id, 'uuid': wallet.uuid, 'balance': str(wallet.balance)})
        )
        logger.info(f"Wallet data for UUID {wallet.uuid} added to cache.")

    except Exception as e:
        logger.error(f"Error writing to Redis: {e}")
