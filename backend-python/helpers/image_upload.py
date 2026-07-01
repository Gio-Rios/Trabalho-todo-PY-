"""Upload de imagens (equivalente a helpers/image-upload.js / multer).

Replica:
- pasta de destino conforme a rota base (users / pets);
- nome do arquivo = timestamp(ms) + numero aleatorio(0-999) + extensao;
- filtro: apenas .png ou .jpg.
"""

import os
import time
import random

from fastapi import HTTPException

ALLOWED_EXT = (".png", ".jpg")


def _folder_from_base_url(base_url: str) -> str:
    if "users" in base_url:
        return "users"
    if "pets" in base_url:
        return "pets"
    return ""


def _check_extension(original_name: str):
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(
            status_code=422,
            detail={"message": "Por favor, envie um arquivo PNG ou JPG!"},
        )
    return ext


async def save_upload(upload_file, base_url: str) -> str:
    """Salva um UploadFile no disco e retorna o filename gerado."""
    ext = _check_extension(upload_file.filename)
    folder = _folder_from_base_url(base_url)

    filename = f"{int(time.time() * 1000)}{random.randint(0, 999)}{ext}"
    dest_dir = os.path.join("public", "images", folder)
    os.makedirs(dest_dir, exist_ok=True)

    dest_path = os.path.join(dest_dir, filename)
    content = await upload_file.read()
    with open(dest_path, "wb") as f:
        f.write(content)

    return filename
