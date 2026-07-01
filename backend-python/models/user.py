"""Model User (equivalente a models/User.js).

O Mongoose definia um Schema com validação e timestamps. Como o
controller original faz a validação manualmente, aqui mantemos a mesma
abordagem e expomos apenas a coleção + um helper para montar o documento
com os campos esperados e os timestamps (createdAt / updatedAt).
"""

from datetime import datetime, timezone

from db.conn import users_collection

User = users_collection


def build_user_doc(name, email, password, phone, image=None):
    now = datetime.now(timezone.utc)
    return {
        "name": name,
        "email": email,
        "password": password,
        "image": image,
        "phone": phone,
        "createdAt": now,
        "updatedAt": now,
    }
