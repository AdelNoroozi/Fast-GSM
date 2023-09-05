from fastapi import APIRouter
from managers import UserManager
from schemas.request import RegisterModel, LoginModel

router = APIRouter(tags=["Auth"])


@router.post("/register/")
async def register(user_data: RegisterModel):
    token = await UserManager.register(user_data.model_dump())
    return {"token": token}


@router.post("/login/")
async def login(user_data: LoginModel):
    token = await UserManager.login(user_data.model_dump())
    return {"token": token}
