"""Rotas de pet (equivalente a routes/PetRoutes.js).

Observação: rotas literais (/mypets, /myadoptions) são declaradas antes
de /{id} para não serem capturadas pela rota com parâmetro — mesmo
comportamento da ordem de declaração do Express.
"""

from fastapi import APIRouter, Request, Depends

from controllers.pet_controller import PetController
from helpers.verify_token import verify_token

router = APIRouter()


@router.post("/create")
async def create(request: Request, _=Depends(verify_token)):
    return await PetController.create(request)


@router.get("/")
async def get_all():
    return await PetController.get_all()


@router.get("/mypets")
async def get_all_user_pets(request: Request, _=Depends(verify_token)):
    return await PetController.get_all_user_pets(request)


@router.get("/myadoptions")
async def get_all_user_adoptions(request: Request, _=Depends(verify_token)):
    return await PetController.get_all_user_adoptions(request)


@router.get("/{id}")
async def get_pet_by_id(id: str, request: Request):
    return await PetController.get_pet_by_id(request, id)


@router.delete("/{id}")
async def remove_pet_by_id(id: str, request: Request, _=Depends(verify_token)):
    return await PetController.remove_pet_by_id(request, id)


@router.patch("/{id}")
async def update_pet(id: str, request: Request, _=Depends(verify_token)):
    return await PetController.update_pet(request, id)


@router.patch("/schedule/{id}")
async def schedule(id: str, request: Request, _=Depends(verify_token)):
    return await PetController.schedule(request, id)


@router.patch("/conclude/{id}")
async def conclude_adoption(id: str, request: Request, _=Depends(verify_token)):
    return await PetController.conclude_adoption(request, id)
