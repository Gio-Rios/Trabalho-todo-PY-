"""Conexão com o MongoDB (equivalente a db/conn.js).

No projeto Node usava-se Mongoose. Aqui usamos o Motor (driver async
oficial do MongoDB para Python), que combina com o estilo async/await
do código original.
"""

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "getapet"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


async def connect():
    # Força uma operação para validar a conexão (o Motor conecta lazy)
    await client.admin.command("ping")
    print("Conectou ao MongoDB com Motor!")


# Coleções (equivalentes aos models do Mongoose)
users_collection = db["users"]
pets_collection = db["pets"]
