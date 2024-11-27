import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from core import db_manager
from core.config import settings
from main import app
from models import Wallet, Operation

client = TestClient(app)

db_manager.init(settings.database_url)

WALLET_UUID = "8f4e3a4d-23a4-4b6e-a3d3-8f4e3a4d23a4"
AMOUNT = 1000.05
OPERATION_ENDPOINT = f"/api/v1/wallets/{WALLET_UUID}/operation"
WALLET_ENDPOINT = f"/api/v1/wallets/{WALLET_UUID}"
BASE_URL = "http://testserver"


class TestCreateOperation:

    @pytest.mark.asyncio
    async def test_create_wallet(self):
        wallet = Wallet(uuid=WALLET_UUID, balance=AMOUNT)
        async with db_manager.session() as session:
            session.add(wallet)
            await session.commit()

    def test_get_wallet_balance(self):
        response = client.get(WALLET_ENDPOINT)
        assert response.status_code == 200

    def test_create_operation_deposit(self):
        operation_request = {"operation_type": "DEPOSIT", "amount": 99.95}

        response = client.post(OPERATION_ENDPOINT, json=operation_request)

        assert response.status_code == 201
        assert response.json()["operation_type"] == "DEPOSIT"
        assert response.json()["amount"] == 99.95

    def test_check_balance_after_deposit(self):
        response = client.get(WALLET_ENDPOINT)

        assert response.status_code == 200
        assert response.json()["balance"] == 1100.00

    def test_create_operation_withdraw(self):
        operation_request = {"operation_type": "WITHDRAW", "amount": 100.00}

        response = client.post(OPERATION_ENDPOINT, json=operation_request)

        assert response.status_code == 201
        assert response.json()["operation_type"] == "WITHDRAW"
        assert response.json()["amount"] == 100.00

    def test_check_balance_after_withdraw(self):
        response = client.get(WALLET_ENDPOINT)

        assert response.status_code == 200
        assert response.json()["balance"] == 1000.00

    @pytest.mark.asyncio
    async def test_delete_wallet(self):
        async with db_manager.session() as session:
            wallet = await session.execute(select(Wallet).filter_by(uuid=WALLET_UUID))
            wallet = wallet.scalars().first()
            operations = await session.execute(select(Operation).filter_by(wallet_id=wallet.id))
            for operation in operations.scalars().all():
                await session.delete(operation)
            await session.delete(wallet)
            await session.commit()


def test_get_operation_correct_uuid():
    response = client.get(OPERATION_ENDPOINT)
    assert response.status_code == 405


def test_post_operation_incorrect_uuid():
    response = client.post(
        "/api/v1/wallets/00000000-0000-0000-0000-000000000000/operation",
        json={"operation_type": "DEPOSIT", "amount": 100.00}
    )
    assert response.status_code == 404


def test_incorrect_field_operation_type():
    operation_request = {"operation_type": "DESPOSITO", "amount": 100.00}
    response = client.post(OPERATION_ENDPOINT, json=operation_request)
    assert response.status_code == 422


def test_incorrect_field_amount():
    amounts = [-100.00, 0.00]

    for amount in amounts:
        operation_request = {"operation_type": "DEPOSIT", "amount": amount}
        response = client.post(OPERATION_ENDPOINT, json=operation_request)
        assert response.status_code == 422


def test_get_wallet_balance_incorrect_uuid():
    response = client.get("/api/v1/wallets/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_post_wallet():
    response = client.post(WALLET_ENDPOINT, json={"balance": 100.00})
    assert response.status_code == 405


def test_delete_wallet():
    response = client.delete(WALLET_ENDPOINT)
    assert response.status_code == 405


def test_update_wallet():
    response = client.put(WALLET_ENDPOINT, json={"balance": 100.00})
    assert response.status_code == 405
