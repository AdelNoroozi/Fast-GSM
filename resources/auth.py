from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers import UserManager, oauth2_scheme, is_superuser
from schemas.request import RegisterModel, LoginModel, AddUserModel
from schemas.response import UserListModel

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data: RegisterModel):
    token = await UserManager.register(user_data.model_dump(), True)
    return {"token": token}


@router.post("/login/", status_code=200)
async def login(user_data: LoginModel):
    token = await UserManager.login(user_data.model_dump())
    return {"token": token}


@router.post("/add-admin/", status_code=201, dependencies=[Depends(oauth2_scheme), Depends(is_superuser)])
async def add_admin(admin_data: AddUserModel):
    admin = await UserManager.add_admin(admin_data.model_dump())
    return {"admin": admin}


@router.get("/users/", status_code=200, response_model=list[UserListModel], dependencies=[Depends(oauth2_scheme)])
async def get_user_list(request: Request):
    user = request.state.user
    return await UserManager.get_user_list(user)
