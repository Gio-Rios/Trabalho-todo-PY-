# GET A PET — Frontend em Python (NiceGUI)

Versão em **Python** do frontend originalmente escrito em **React**.
Mantém a mesma estrutura de componentes, as mesmas rotas e o mesmo visual.

Para portar uma SPA React (componentes + rotas + reatividade) para Python
puro, usamos o **NiceGUI**: toda a interface é escrita em Python (sem
HTML/JSX/JS), com páginas, navegação e componentes, e ele sobe o próprio
servidor web.

## Equivalência com o original

| React (original) | Python (esta versão) |
|------------------|----------------------|
| react / react-dom | NiceGUI |
| react-router-dom (`<Routes>`) | `@ui.page('/...')` |
| `<Link>` | `ui.link(...)` |
| Componente `.js` (função JSX) | Função Python que monta `ui.*` |
| `index.css` | `styles.py` (CSS injetado via `ui.add_head_html`) |
| `src/assets` | `assets/` servido por `app.add_static_files` |

## Estrutura (espelha a do React)

```
frontend-python/
├── main.py                       # ≈ src/index.js + src/App.js (entry + rotas)
├── styles.py                     # ≈ src/index.css
├── requirements.txt
├── assets/
│   └── img/logo.png              # ≈ src/assets/img/logo.png
└── components/
    ├── layout/
    │   ├── navbar.py             # ≈ Navbar.js
    │   └── footer.py             # ≈ Footer.js
    └── pages/
        ├── home.py               # ≈ Home.js
        └── auth/
            ├── login.py          # ≈ Login.js
            └── register.py       # ≈ Register.js
```

## Rotas

- `/`         → Home
- `/login`    → Login
- `/register` → Register

(São as mesmas três rotas do `App.js` original. As páginas são placeholders
com um `<h1>`, exatamente como no React original.)

## Como rodar

```bash
cd frontend-python
pip install -r requirements.txt
python main.py
```

Abra **http://localhost:3000** no navegador (mesma porta do React, que é a
origem liberada no CORS do backend).

Dica: para recarregar automaticamente ao salvar (como o hot reload do
`npm start`), troque `reload=False` por `reload=True` no `main.py`.
