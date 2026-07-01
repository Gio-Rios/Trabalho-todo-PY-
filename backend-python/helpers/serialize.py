"""Utilitário para serializar documentos do MongoDB em JSON.

O Mongoose convertia automaticamente _id (ObjectId) em string e datas
em ISO ao responder em JSON. Aqui replicamos esse comportamento.
"""

from datetime import datetime

from bson import ObjectId


def serialize(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [serialize(v) for v in value]
    if isinstance(value, dict):
        return {k: serialize(v) for k, v in value.items()}
    return value
