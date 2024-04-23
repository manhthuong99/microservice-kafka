from fastapi import APIRouter, Depends
from ...domain.services.promotion_service import PromotionService

router = APIRouter()


@router.post("/post")
async def save(promotion: dict, promotion_service=Depends(PromotionService)):
    return await promotion_service.save(promotion)


@router.put("/apply/{coupon}")
async def apply(coupon: str, promotion_service=Depends(PromotionService)):
    return await promotion_service.apply(coupon)
