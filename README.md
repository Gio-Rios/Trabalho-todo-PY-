# GET A PET — Projeto completo em Python

Porte completo do projeto **15_GET_A_PET** de **JavaScript para Python**,
sem exceção: backend e frontend.

| Parte | Original (JS) | Agora (Python) |
|-------|---------------|----------------|
| Backend | Node.js + Express + Mongoose | **FastAPI + Motor (MongoDB)** |
| Frontend | React + react-router | **NiceGUI** (UI 100% em Python) |
| Banco | MongoDB | MongoDB (igual) |

```
15_GET_A_PET-python/
├── docker-compose.yml      # MongoDB
├── backend-python/         # API (FastAPI)  -> porta 5000
└── frontend-python/        # UI  (NiceGUI)  -> porta 3000
```

## Como rodar (3 passos)

### 1. Banco de dados
```bash
docker compose up -d        # sobe o MongoDB em localhost:27017
```
(ou tenha um MongoDB local rodando)

### 2. Backend (API) — porta 5000
```bash
cd backend-python
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```
Docs interativas: http://localhost:5000/docs

### 3. Frontend (UI) — porta 3000
Em outro terminal:
```bash
cd frontend-python
pip install -r requirements.txt
python main.py
```
Abra http://localhost:3000

O frontend (porta 3000) é a origem já liberada no CORS do backend, então
os dois conversam sem ajustes.

## Detalhes

Cada pasta tem seu próprio `README.md` com a tabela de equivalência
arquivo-a-arquivo em relação ao código JavaScript original e observações
sobre fidelidade (rotas, status codes, validações, etc.).
