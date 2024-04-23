from fastapi import APIRouter, Depends
from ...domain.services.product_service import ProductService

router = APIRouter()


@router.get("/get/{id}")
async def get_by_id(id: str, product_service=Depends(ProductService)):
    return await product_service.get_by_id(id)


@router.post("/post")
async def save(product: dict, product_service=Depends(ProductService)):
    return await product_service.save(product)
