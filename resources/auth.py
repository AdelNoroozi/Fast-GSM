from fastapi import APIRouter
from managers import UserManager
from schemas.request import RegisterModel, LoginModel

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data: RegisterModel):
    token = await UserManager.register(user_data.model_dump())
    return {"token": token}


@router.post("/login/", status_code=200)
async def login(user_data: LoginModel):
    token = await UserManager.login(user_data.model_dump())
    return {"token": token}
