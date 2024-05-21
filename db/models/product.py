from sqlalchemy import BigInteger, VARCHAR, ForeignKey, select, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import CreatedModel, db
from db.utils import CustomImageField


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')


class Product(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    author: Mapped[str] = mapped_column(VARCHAR(255))
    genre: Mapped[str] = mapped_column(VARCHAR(255))
    translater: Mapped[str] = mapped_column(VARCHAR(255))
    page_count: Mapped[int] = mapped_column(Integer)
    cover: Mapped[str] = mapped_column(VARCHAR(20))
    # photo: Mapped[str] = mapped_column(CustomImageField)
    price: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    photo: Mapped[str] = mapped_column(VARCHAR(255))
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', back_populates='products')

    @classmethod
    async def get_products_by_category_id(cls, category_id):
        query = select(cls).where(cls.category_id == category_id)
        return (await db.execute(query)).scalars()
