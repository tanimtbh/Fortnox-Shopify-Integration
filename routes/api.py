from fastapi import APIRouter
from webhooks_shopify.webhooks import shopify
from products import product
from users import user



router = APIRouter()
#router.include_router(product.router)
router.include_router(user.router)
router.include_router(shopify.router)
router.include_router(product.router)

