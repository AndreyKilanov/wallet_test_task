from fastapi import APIRouter
from api.v1 import wallet_router

main_router = APIRouter(prefix='/api')

main_router.include_router(
    wallet_router,
    prefix='/v1',
    tags=['API WALLETS V1'],
    responses={404: {'description': 'Not found'}}
)
