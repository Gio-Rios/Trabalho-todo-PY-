"""Middleware para validar o token (equivalente a helpers/verify-token.js).

No Express era um middleware (req, res, next). No FastAPI usamos uma
*dependency*: ela valida o token e devolve o payload decodificado, que
fica disponível para o controller como `req.user` ficava no original.
Em caso de falha, lança HTTPException com o mesmo status/mensagem.
"""

import jwt
from fastapi import Request, HTTPException

from helpers.get_token import get_token

SECRET = "nossosecret"


async def verify_token(request: Request):
    if not request.headers.get("authorization"):
        raise HTTPException(status_code=401, detail={"message": "Acesso Negado!"})

    token = get_token(request)

    if not token:
        raise HTTPException(status_code=401, detail={"message": "Acesso Negado!"})

    try:
        verified = jwt.decode(token, SECRET, algorithms=["HS256"])
        return verified
    except Exception:
        raise HTTPException(status_code=400, detail={"message": "Token inválido!"})
