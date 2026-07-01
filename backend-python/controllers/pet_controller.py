"""PetController (equivalente a controllers/PetController.js)."""

import os

from bson import ObjectId
from fastapi import Request
from fastapi.responses import JSONResponse

from models.pet import Pet, build_pet_doc
from helpers.get_token import get_token
from helpers.get_user_by_token import get_user_by_token
from helpers.image_upload import save_upload
from helpers.serialize import serialize


def validate_fields(fields: dict, body: dict):
    for field, message in fields.items():
        value = body.get(field)
        if value is None or value == "":
            return {"valid": False, "message": message}
    return {"valid": True}


async def validate_pet_ownership(request: Request, pet_id: str):
    """Verifica se o pet existe e pertence ao usuário logado.

    Retorna (pet, None) em caso de sucesso ou (None, JSONResponse) com o erro.
    """
    if not ObjectId.is_valid(pet_id):
        return None, JSONResponse(status_code=422, content={"message": "ID inválido"})

    pet = await Pet.find_one({"_id": ObjectId(pet_id)})
    if not pet:
        return None, JSONResponse(status_code=404, content={"message": "Pet não encontrado!"})

    token = get_token(request)
    user = await get_user_by_token(token)

    if str(pet["user"]["_id"]) != str(user["_id"]):
        return None, JSONResponse(
            status_code=422,
            content={
                "message": "Houve um problema em processar a sua solicitação, "
                "tente novamente mais tarde!"
            },
        )

    return pet, None


class PetController:
    @staticmethod
    async def create(request: Request):
        form = await request.form()
        name = form.get("name")
        age = form.get("age")
        weight = form.get("weight")
        color = form.get("color")
        images = form.getlist("images")
        available = True

        validations = {
            "name": "O nome é obrigatório!",
            "age": "A idade é obrigatória!",
            "weight": "O peso é obrigatório!",
            "color": "A cor é obrigatória!",
        }
        body = {"name": name, "age": age, "weight": weight, "color": color}
        validation = validate_fields(validations, body)
        if not validation["valid"]:
            return JSONResponse(status_code=422, content={"message": validation["message"]})

        # filtra apenas uploads reais
        images = [img for img in images if getattr(img, "filename", "")]
        if len(images) == 0:
            return JSONResponse(status_code=422, content={"message": "A imagem é obrigatória!"})

        token = get_token(request)
        user = await get_user_by_token(token)

        saved_images = []
        for image in images:
            saved_images.append(await save_upload(image, request.url.path))

        doc = build_pet_doc(
            name=name,
            age=age,
            weight=weight,
            color=color,
            available=available,
            images=saved_images,
            user={
                "_id": str(user["_id"]),
                "name": user["name"],
                "image": user.get("image"),
                "phone": user["phone"],
            },
        )

        try:
            result = await Pet.insert_one(doc)
            doc["_id"] = result.inserted_id
            # mantém o status 301 do projeto original
            return JSONResponse(
                status_code=301,
                content={"message": "Pet cadastrado com sucesso!", "newPet": serialize(doc)},
            )
        except Exception as error:
            return JSONResponse(status_code=500, content={"message": str(error)})

    @staticmethod
    async def get_all():
        cursor = Pet.find().sort("createdAt", -1)
        pets = await cursor.to_list(length=None)
        return JSONResponse(status_code=200, content={"pets": serialize(pets)})

    @staticmethod
    async def get_all_user_pets(request: Request):
        token = get_token(request)
        user = await get_user_by_token(token)

        cursor = Pet.find({"user._id": str(user["_id"])}).sort("createdAt", -1)
        pets = await cursor.to_list(length=None)
        return JSONResponse(status_code=200, content={"pets": serialize(pets)})

    @staticmethod
    async def get_all_user_adoptions(request: Request):
        token = get_token(request)
        user = await get_user_by_token(token)

        cursor = Pet.find({"adopter._id": str(user["_id"])}).sort("createdAt", -1)
        pets = await cursor.to_list(length=None)
        return JSONResponse(status_code=200, content={"pets": serialize(pets)})

    @staticmethod
    async def get_pet_by_id(request: Request, pet_id: str):
        pet, error = await validate_pet_ownership(request, pet_id)
        if error:
            return error
        return JSONResponse(status_code=200, content={"pet": serialize(pet)})

    @staticmethod
    async def remove_pet_by_id(request: Request, pet_id: str):
        pet, error = await validate_pet_ownership(request, pet_id)
        if error:
            return error

        # remove imagens associadas ao pet
        for image in pet.get("images", []):
            image_path = os.path.join("public", "images", "pets", image)
            if os.path.exists(image_path):
                os.remove(image_path)

        await Pet.find_one_and_delete({"_id": ObjectId(pet_id)})
        return JSONResponse(status_code=200, content={"message": "Pet removido com sucesso!"})

    @staticmethod
    async def update_pet(request: Request, pet_id: str):
        pet, error = await validate_pet_ownership(request, pet_id)
        if error:
            return error

        form = await request.form()
        name = form.get("name")
        age = form.get("age")
        weight = form.get("weight")
        color = form.get("color")
        available = form.get("available")
        images = [img for img in form.getlist("images") if getattr(img, "filename", "")]

        updated_data = {}

        validations = {
            "name": "O nome é obrigatório!",
            "age": "A idade é obrigatória!",
            "weight": "O peso é obrigatório!",
            "color": "A cor é obrigatória!",
        }
        body = {"name": name, "age": age, "weight": weight, "color": color}
        validation = validate_fields(validations, body)
        if not validation["valid"]:
            return JSONResponse(status_code=422, content={"message": validation["message"]})
        else:
            updated_data["name"] = name
            updated_data["age"] = age
            updated_data["weight"] = weight
            updated_data["color"] = color
            updated_data["available"] = available if available is not None else True

        # remove imagens antigas se novas imagens forem enviadas
        if images and len(images) > 0:
            for image in pet.get("images", []):
                image_path = os.path.join("public", "images", "pets", image)
                if os.path.exists(image_path):
                    os.remove(image_path)

            updated_data["images"] = []
            for image in images:
                updated_data["images"].append(await save_upload(image, request.url.path))

        try:
            await Pet.find_one_and_update({"_id": ObjectId(pet_id)}, {"$set": updated_data})
            return JSONResponse(
                status_code=200, content={"message": "Pet atualizado com sucesso!"}
            )
        except Exception as error:
            return JSONResponse(status_code=500, content={"message": str(error)})

    @staticmethod
    async def schedule(request: Request, pet_id: str):
        pet = await Pet.find_one({"_id": ObjectId(pet_id)})

        if not pet:
            return JSONResponse(status_code=404, content={"message": "Pet não encontrado!"})

        token = get_token(request)
        user = await get_user_by_token(token)

        if str(pet["user"]["_id"]) == str(user["_id"]):
            return JSONResponse(
                status_code=422,
                content={"message": "Não é permitido agendar visita para o seu próprio Pet!"},
            )

        if pet.get("adopter"):
            if str(pet["adopter"]["_id"]) == str(user["_id"]):
                return JSONResponse(
                    status_code=422,
                    content={"message": "Você já agendou uma visita para este Pet!"},
                )

        pet["adopter"] = {
            "_id": str(user["_id"]),
            "name": user["name"],
            "image": user.get("image"),
        }

        await Pet.find_one_and_update({"_id": ObjectId(pet_id)}, {"$set": {"adopter": pet["adopter"]}})

        return JSONResponse(
            status_code=200,
            content={
                "message": "A visita foi agendada com sucesso, entre em contato com "
                f"{pet['user']['name']} pelo telefone {pet['user']['phone']}"
            },
        )

    @staticmethod
    async def conclude_adoption(request: Request, pet_id: str):
        pet = await Pet.find_one({"_id": ObjectId(pet_id)})

        if not pet:
            return JSONResponse(status_code=404, content={"message": "Pet não encontrado!"})

        token = get_token(request)
        user = await get_user_by_token(token)

        if str(pet["user"]["_id"]) != str(user["_id"]):
            return JSONResponse(
                status_code=422,
                content={
                    "message": "Houve um problema em processar a sua solicitação, "
                    "tente novamente mais tarde!"
                },
            )

        await Pet.find_one_and_update({"_id": ObjectId(pet_id)}, {"$set": {"available": False}})

        return JSONResponse(
            status_code=200,
            content={"message": "Parabéns o ciclo de adoção foi finalizado com sucesso"},
        )
