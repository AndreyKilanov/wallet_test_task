import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Wallet


async def _validate_wallet_uuid(wallet_uuid: str, session: AsyncSession) -> Wallet:
    """
    Валидатор UUID кошелька.

    :param wallet_uuid: UUID кошелька
    :param session: сессия БД
    :return: объект Wallet, если он существует
    :raises HTTPException: 400 - если UUID имеет неверный формат
    :raises HTTPException: 404 - если кошелек не найден
    """
    try:
        uuid.UUID(wallet_uuid, version=4)

    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid wallet UUID')

    wallet = await session.execute(select(Wallet).filter_by(uuid=wallet_uuid))
    wallet = wallet.scalars().first()

    if not wallet:
        raise HTTPException(status_code=404, detail='Wallet not found')

    return wallet


def _validate_operation_type(operation_type: str) -> str:
    """
    Валидатор типа операции.

    :param operation_type: тип операции (DEPOSIT или WITHDRAW)
    :return: тип операции, если он валидный
    :raises HTTPException: 400 - если тип операции не валидный
    """
    if operation_type not in ['DEPOSIT', 'WITHDRAW']:
        raise HTTPException(status_code=400, detail='Invalid operation type')

    return operation_type
