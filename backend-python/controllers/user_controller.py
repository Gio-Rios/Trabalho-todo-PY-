"""UserController (equivalente a controllers/UserController.js)."""

import os

import bcrypt
import jwt
from bson import ObjectId
from fastapi import Request
from fastapi.responses import JSONResponse

from models.user import User, build_user_doc
from helpers.create_user_token import create_user_token
from helpers.get_token import get_token
from helpers.get_user_by_token import get_user_by_token
from helpers.image_upload import save_upload
from helpers.serialize import serialize

SECRET = "nossosecret"


def validate_fields(fields: dict, body: dict):
    """Equivalente à função validateFields do original."""
    for field, message in fields.items():
        if not body.get(field):
            return {"valid": False, "message": message}
    return {"valid": True}


class UserController:
    @staticmethod
    async def register(request: Request):
        body = await request.json()
        name = body.get("name")
        email = body.get("email")
        phone = body.get("phone")
        password = body.get("password")
        confirmpassword = body.get("confirmpassword")

        validations = {
            "name": "O nome é obrigatório!",
            "email": "O email é obrigatório!",
            "phone": "O telefone é obrigatório!",
            "password": "A senha é obrigatória!",
            "confirmpassword": "A confirmação de senha é obrigatória!",
        }

        validation = validate_fields(validations, body)
        if not validation["valid"]:
            return JSONResponse(status_code=422, content={"message": validation["message"]})

        if password != confirmpassword:
            return JSONResponse(status_code=422, content={"message": "As senhas não condizem!"})

        # checa se o usuário já existe
        user_exists = await User.find_one({"email": email})
        if user_exists:
            return JSONResponse(
                status_code=422, content={"message": "Por favor, utilize outro e-mail!"}
            )

        # cria o hash da senha
        salt = bcrypt.gensalt(12)
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        doc = build_user_doc(name=name, email=email, phone=phone, password=password_hash)

        try:
            result = await User.insert_one(doc)
            doc["_id"] = result.inserted_id
            return create_user_token(doc)
        except Exception as error:
            return JSONResponse(status_code=500, content={"message": str(error)})

    @staticmethod
    async def login(request: Request):
        body = await request.json()
        email = body.get("email")
        password = body.get("password")

        validations = {
            "email": "O email é obrigatório!",
            "password": "A senha é obrigatória!",
        }

        validation = validate_fields(validations, body)
        if not validation["valid"]:
            return JSONResponse(status_code=422, content={"message": validation["message"]})

        user = await User.find_one({"email": email})

        if not user:
            return JSONResponse(
                status_code=422, content={"message": "Usuário ou senha inválidos!"}
            )

        is_match = bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8"))
        if not is_match:
            return JSONResponse(
                status_code=422, content={"message": "Usuário ou senha inválidos!"}
            )

        try:
            return create_user_token(user)
        except Exception as error:
            return JSONResponse(status_code=500, content={"message": str(error)})

    @staticmethod
    async def check_user(request: Request):
        current_user = None

        if request.headers.get("authorization"):
            token = get_token(request)
            decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
            current_user = await User.find_one({"_id": ObjectId(decoded["id"])})
            if current_user:
                current_user.pop("password", None)

        return JSONResponse(status_code=200, content=serialize(current_user))

    @staticmethod
    async def get_user_by_id(user_id: str):
        try:
            oid = ObjectId(user_id)
        except Exception:
            return JSONResponse(status_code=422, content={"message": "Usuário não encontrado!"})

        user = await User.find_one({"_id": oid}, {"password": 0})

        if not user:
            return JSONResponse(status_code=422, content={"message": "Usuário não encontrado!"})

        return JSONResponse(status_code=200, content={"user": serialize(user)})

    @staticmethod
    async def edit_user(request: Request, user_id: str):
        # checa se o usuário existe
        token = get_token(request)
        user = await get_user_by_token(token)

        form = await request.form()
        name = form.get("name")
        email = form.get("email")
        phone = form.get("phone")
        password = form.get("password")
        confirmpassword = form.get("confirmpassword")

        image_file = form.get("image")
        if image_file is not None and getattr(image_file, "filename", ""):
            # remove imagem antiga, se existir
            if user.get("image"):
                old_image_path = os.path.join("public", "images", "users", user["image"])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            user["image"] = await save_upload(image_file, request.url.path)

        validations = {
            "name": "O nome é obrigatório!",
            "email": "O email é obrigatório!",
            "phone": "O telefone é obrigatório!",
        }
        body = {"name": name, "email": email, "phone": phone}
        validation = validate_fields(validations, body)
        if not validation["valid"]:
            return JSONResponse(status_code=422, content={"message": validation["message"]})

        user_exists = await User.find_one({"email": email})

        # checa se o email já está em uso por outro usuário
        if user["email"] != email and user_exists:
            return JSONResponse(
                status_code=422, content={"message": "Por favor utilize outro e-mail!"}
            )

        user["name"] = name
        user["email"] = email
        user["phone"] = phone

        if password != confirmpassword:
            return JSONResponse(status_code=422, content={"message": "As senhas não condizem!"})
        elif password == confirmpassword and password is not None and password != "":
            salt = bcrypt.gensalt(12)
            password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
            user["password"] = password_hash

        try:
            update = {k: v for k, v in user.items() if k != "_id"}
            await User.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": update})
            return JSONResponse(
                status_code=200, content={"message": "Usuário atualizado com sucesso!"}
            )
        except Exception as error:
            return JSONResponse(status_code=500, content={"message": str(error)})
