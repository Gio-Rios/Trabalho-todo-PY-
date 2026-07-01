"""Ponto de entrada da aplicação (equivalente a index.js).

Roda em http://localhost:5000 (igual ao projeto Node).
Inicie com:  uvicorn main:app --host 0.0.0.0 --port 5000
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db.conn import connect
from routes.user_routes import router as user_router
from routes.pet_routes import router as pet_router

app = FastAPI(title="GET A PET API")

# Resolve CORS (equivalente a cors({ credentials, origin }))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await connect()


# Rotas
app.include_router(user_router, prefix="/users")
app.include_router(pet_router, prefix="/pets")

# Pasta pública para imagens (equivalente a express.static('public')).
# As imagens ficam em public/images/... e são servidas em /images/...
os.makedirs(os.path.join("public", "images", "users"), exist_ok=True)
os.makedirs(os.path.join("public", "images", "pets"), exist_ok=True)
app.mount("/images", StaticFiles(directory=os.path.join("public", "images")), name="images")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
