from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.product_image import ProductImage

async def filter_products(
    min_price: float,
    max_price: float,
    sort_by: str | None,
    sort_order: str | None,
    condition: str | None,
    category: list[str],
    db: AsyncSession
):
    filters = []
    if min_price > 0:
        filters.append(
            Product.price > min_price
        )
        if max_price > min_price:
            filters.append(
                Product.price < max_price
            )

    if condition.lower() in ["used", "new", "repack"]:
        filters.append(
            Product.condition == condition.lower()
        )

    if len(category) > 0:
        filters.append(
            Product.category_id.in_(category)
        )

    stmnt = select(
        Product.name, 
        Product.price, 
        Product.category,
        Product.id,
        Product.rating,
        Product.images
    ).options(
        selectinload(
            Product.images.and_(
                ProductImage.image_type == "thumb"
            )
        ).load_only(
            ProductImage.id,
            ProductImage.url
        )
    ).where(*filters)

    if sort_by.lower() in ["name", "price"]:
        if sort_order.lower() == "dsc":
            stmnt = stmnt.order_by(
                Product.name.asc() if sort_by.lower() == "name" else Product.price.asc()
            )
        else:
            stmnt = stmnt.order_by(
                Product.name.desc() if sort_by.lower() == "name" else Product.price.desc()
            )

    result = await db.execute(stmnt)

    products = result.all()

    return products