from sqlalchemy import BigInteger, VARCHAR, ForeignKey, select, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import CreatedModel, db


class Order(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    count: Mapped[int] = mapped_column(BigInteger, nullable=False)
