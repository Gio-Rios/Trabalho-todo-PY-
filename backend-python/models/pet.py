"""Model Pet (equivalente a models/Pet.js)."""

from datetime import datetime, timezone

from db.conn import pets_collection

Pet = pets_collection


def build_pet_doc(name, age, weight, color, images, user, available=True, adopter=None):
    now = datetime.now(timezone.utc)
    return {
        "name": name,
        "age": age,
        "weight": weight,
        "color": color,
        "images": images,
        "available": available,
        "user": user,
        "adopter": adopter,
        "createdAt": now,
        "updatedAt": now,
    }
