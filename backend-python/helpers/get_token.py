"""Extrai o token do header Authorization: 'Bearer <token>'.

Equivalente a helpers/get-token.js.
"""

from fastapi import Request


def get_token(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header:
        return None
    parts = auth_header.split(" ")
    if len(parts) < 2:
        return None
    return parts[1]
