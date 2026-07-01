# GET A PET — Backend em Python (FastAPI)

Versão em **Python** do backend originalmente escrito em **Node.js/Express**.
Mantém as **mesmas rotas, métodos, status codes e formato de resposta JSON**,
então o frontend React existente continua funcionando sem alterações.

## Stack (equivalência com o original)

| Node.js (original) | Python (esta versão) |
|--------------------|----------------------|
| Express            | FastAPI              |
| Mongoose           | Motor (driver async do MongoDB) |
| jsonwebtoken       | PyJWT                |
| bcrypt             | bcrypt               |
| multer             | UploadFile + helper próprio |
| cors               | CORSMiddleware       |
| express.static     | StaticFiles          |
| nodemon            | uvicorn --reload     |

## Estrutura

```
backend-python/
├── main.py                  # ≈ index.js (app, CORS, static, rotas)
├── requirements.txt
├── db/conn.py               # ≈ db/conn.js
├── models/
│   ├── user.py              # ≈ models/User.js
│   └── pet.py               # ≈ models/Pet.js
├── helpers/
│   ├── create_user_token.py
│   ├── get_token.py
│   ├── get_user_by_token.py
│   ├── verify_token.py      # middleware -> dependency do FastAPI
│   ├── image_upload.py      # ≈ multer
│   └── serialize.py         # ObjectId/datas -> JSON
├── controllers/
│   ├── user_controller.py   # ≈ controllers/UserController.js
│   └── pet_controller.py    # ≈ controllers/PetController.js
└── routes/
    ├── user_routes.py       # ≈ routes/UserRoutes.js
    └── pet_routes.py        # ≈ routes/PetRoutes.js
```

## Como rodar

1. Suba o MongoDB (mesmo do projeto original):
   ```bash
   docker compose up -d   # usa o docker-compose.yml com o serviço mongo
   ```
   ou tenha um MongoDB local em `mongodb://localhost:27017`.

2. Instale as dependências:
   ```bash
   cd backend-python
   pip install -r requirements.txt
   ```

3. Inicie o servidor (porta 5000, igual ao Node):
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
   ```

Documentação interativa automática em `http://localhost:5000/docs`.

## Endpoints

**Usuários** (`/users`)
- `POST /register`
- `POST /login`
- `GET  /checkuser`
- `GET  /{id}`
- `PATCH /edit/{id}` (autenticado, com upload de imagem)

**Pets** (`/pets`)
- `POST /create` (autenticado, upload de múltiplas imagens)
- `GET  /`
- `GET  /mypets` (autenticado)
- `GET  /myadoptions` (autenticado)
- `GET  /{id}`
- `DELETE /{id}` (autenticado)
- `PATCH /{id}` (autenticado, upload de imagens)
- `PATCH /schedule/{id}` (autenticado)
- `PATCH /conclude/{id}` (autenticado)

Imagens enviadas ficam em `public/images/users` e `public/images/pets`,
servidas em `http://localhost:5000/images/...`.

## Observações sobre fidelidade ao original

- O endpoint de criação de pet responde com **status 301** — preservado
  exatamente como no código Node original (é incomum para um POST, mas foi
  mantido para não mudar o comportamento).
- A validação de campos é feita manualmente nos controllers, retornando
  `422` com as mesmas mensagens em português do projeto original.
- O segredo do JWT (`nossosecret`) foi mantido igual. Em produção, mova-o
  para uma variável de ambiente.
