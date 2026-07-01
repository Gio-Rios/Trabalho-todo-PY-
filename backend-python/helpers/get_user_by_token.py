"""Recupera o usuário a partir do JWT.

Equivalente a helpers/get-user-by-token.js. (No original havia um bug que
referenciava `res` fora de escopo quando o token era nulo; aqui apenas
retornamos None nesse caso.)
"""

import jwt
from bson import ObjectId

from models.user import User

SECRET = "nossosecret"


async def get_user_by_token(token):
    if not token:
        return None

    decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
    user_id = decoded["id"]

    user = await User.find_one({"_id": ObjectId(user_id)})
    return user
