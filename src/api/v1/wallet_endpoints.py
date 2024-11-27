import json
from decimal import Decimal

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import _validate_wallet_uuid
from cache import add_data_to_cache, redis_cache
from core import get_async_session
from models import Wallet, Operation
from schemas.operation_schema import OperationSchemaResponse, OperationSchemaRequest
from schemas.wallet_schema import WalletSchemaResponse

router = APIRouter(prefix='/wallets')


@router.post('/{wallet_uuid}/operation', response_model=OperationSchemaResponse, status_code=201)
async def create_operation(
        wallet_uuid: str,
        operation_request: OperationSchemaRequest,
        session: AsyncSession = Depends(get_async_session)
) -> Operation:
    try:
        async with session.begin():
            wallet = await _validate_wallet_uuid(wallet_uuid, session)
            operation = Operation(
                wallet_id=wallet.id,
                operation_type=operation_request.operation_type,
                amount=operation_request.amount
            )
            amount = Decimal(operation_request.amount)

            match operation_request.operation_type:
                case 'DEPOSIT':
                    wallet.balance += amount
                case 'WITHDRAW':
                    if wallet.balance < amount:
                        raise HTTPException(status_code=400, detail='Insufficient balance')
                    wallet.balance -= amount

            session.add_all([operation, wallet])
            await session.commit()

            add_data_to_cache(wallet)

            return operation

    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail='Invalid request body') from e

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error') from e


@router.get('/{wallet_uuid}', response_model=WalletSchemaResponse, status_code=200)
async def get_wallet_balance(
        wallet_uuid: str,
        session: AsyncSession = Depends(get_async_session)
) -> Wallet:
    try:
        wallet_cache = redis_cache.get(wallet_uuid)

        if wallet_cache:
            return json.loads(wallet_cache)

        wallet = await _validate_wallet_uuid(wallet_uuid, session)

        add_data_to_cache(wallet)

        return wallet

    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail='Invalid request body') from e

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error') from e
