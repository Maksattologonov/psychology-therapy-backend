from fastapi import APIRouter

from apis import accounts

router = APIRouter()
router.include_router(accounts.router)
