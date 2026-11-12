from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import math
from typing import Annotated

from app.services.product import filter_products
from app.schemas.product import ProductsResponse, ProductResponse
from app.configs.db import get_db
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category

router = APIRouter()
DBSession = Annotated[AsyncSession, Depends(get_db)]

@router.get("/", response_model=list[ProductsResponse])
async def get_products(
    db: DBSession,
    min_price: float = Query(default=0),
    max_price: float = Query(default=math.inf),
    sort_by: str | None = Query(default=None, alias="sort"),
    sort_order: str | None = Query(default=None, alias="order"),
    condition: str | None = Query(default=None),
    category: Annotated[list[str] | None, Query()] = None
):
    categories = category if type(category) == list else []
    products = await filter_products(min_price, max_price, sort_by, sort_order, condition, categories, db)

    products = [ProductsResponse.model_validate(product) for product in products]

    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(db: DBSession, product_id: str):
    result = await db.execute(
        select(Product).options(
            selectinload(Product.images).load_only(
                ProductImage.id,
                ProductImage.url
            ),
            selectinload(Product.category).load_only(
                Category.id,
                Category.image_url,
                Category.name
            )
        ).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product = ProductResponse.model_validate(product)

    return product
