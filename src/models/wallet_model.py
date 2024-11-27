from pydantic import UUID4
from sqlalchemy import Integer, ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[UUID4] = mapped_column(String, unique=True)
    balance: Mapped[float] = mapped_column(Float(asdecimal=True, decimal_return_scale=2), default=0)

    def __repr__(self):
        return f'Wallet(uuid={self.uuid}, balance={self.balance})'


class Operation(Base):
    __tablename__ = 'operations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey('wallets.id'))
    operation_type: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)

    wallet: Mapped['Wallet'] = relationship("Wallet", backref='operations', lazy='selectin')

    def __repr__(self):
        return (
            f'Operation(wallet_id={self.wallet_id},'
            f'operation_type={self.operation_type},'
            f'amount={self.amount})'
        )
