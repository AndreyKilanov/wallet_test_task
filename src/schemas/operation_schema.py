from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, PositiveFloat, UUID4, field_validator


class OperationType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class OperationSchemaRequest(BaseModel):
    operation_type: OperationType
    amount: PositiveFloat = Decimal(0.00)

    @field_validator('amount', mode='before')
    @classmethod
    def validate_amount(cls, value) -> float:
        if value < 0:
            raise ValueError('Amount must be positive')

        if round(float(value), 2) != float(value):
            raise ValueError('Amount must have no more than 2 decimal places')

        return value


class OperationSchemaResponse(OperationSchemaRequest):
    model_config = ConfigDict(from_attributes=True)
    id: int
    wallet_id: int
