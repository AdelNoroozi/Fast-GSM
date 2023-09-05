from fastapi import APIRouter
from managers import UserManager
from schemas.request import RegisterModel

router = APIRouter(tags=["Auth"])


@router.post("/register/")
async def register(user_data: RegisterModel):
    token = await UserManager.register(user_data.model_dump())
    return {"token": token}
