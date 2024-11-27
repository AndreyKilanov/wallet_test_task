# import asyncio
import logging
import random
import uuid

from core import db_manager
# from core.config import settings
from models import Wallet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def creating_test_wallets(wallet_uuid: str = None, balance: float = None) -> str:
    try:
        uuid.UUID(wallet_uuid, version=4)

    except ValueError:
        logger.error('Invalid wallet UUID')

    async with db_manager.session() as session:
        wallet = Wallet(
            uuid=str(uuid.uuid4()) if wallet_uuid is None else wallet_uuid,
            balance=float(
                format(random.uniform(0.01, 10000.00), '.2f')
            ) if balance is None else float(balance)
        )
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)

        logger.info(f'Wallet {wallet.uuid} created with balance {wallet.balance}')
        return wallet.uuid
