"""Rotas de usuário (equivalente a routes/UserRoutes.js)."""

from fastapi import APIRouter, Request, Depends

from controllers.user_controller import UserController
from helpers.verify_token import verify_token

router = APIRouter()


@router.post("/register")
async def register(request: Request):
    return await UserController.register(request)


@router.post("/login")
async def login(request: Request):
    return await UserController.login(request)


@router.get("/checkuser")
async def check_user(request: Request):
    return await UserController.check_user(request)


@router.get("/{id}")
async def get_user_by_id(id: str):
    return await UserController.get_user_by_id(id)


@router.patch("/edit/{id}")
async def edit_user(id: str, request: Request, _=Depends(verify_token)):
    return await UserController.edit_user(request, id)
