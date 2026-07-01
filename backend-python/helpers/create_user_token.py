"""Gera o JWT e devolve a resposta de autenticação.

Equivalente a helpers/create-user-token.js.
"""

import jwt
from fastapi.responses import JSONResponse

SECRET = "nossosecret"


def create_user_token(user):
    token = jwt.encode(
        {
            "name": user["name"],
            "id": str(user["_id"]),
        },
        SECRET,
        algorithm="HS256",
    )

    return JSONResponse(
        status_code=200,
        content={
            "message": "Autenticado com sucesso",
            "token": token,
            "userId": str(user["_id"]),
        },
    )
