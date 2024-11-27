from decimal import Decimal

from pydantic import BaseModel, UUID4, PositiveFloat, ConfigDict


class WalletSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    uuid: UUID4
    balance: PositiveFloat = Decimal(0.00)
