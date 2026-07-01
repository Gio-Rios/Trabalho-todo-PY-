"""Página Login."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def login_content():
    with ui.element("section"):
        with ui.element("div").style("max-width:460px; margin:2em auto;"):
            ui.label("Entrar").style(
                "font-size:2.1em; font-weight:bold; color:#16479D; margin-bottom:1em; display:block;"
            )

            email_input = ui.input(label="E-mail", placeholder="Digite o seu e-mail").style("width:100%;")
            password_input = ui.input(
                label="Senha",
                placeholder="Digite a sua senha",
                password=True,
                password_toggle_button=True,
            ).style("width:100%;")

            error_msg = ui.label("").style("color:#d32f2f; font-size:0.92em; margin-top:0.3em;")

            async def do_login():
                error_msg.set_text("")
                email_val = email_input.value.strip()
                password_val = password_input.value
                if not email_val or not password_val:
                    error_msg.set_text("Preencha todos os campos!")
                    return
                try:
                    async with httpx.AsyncClient() as client:
                        r = await client.post(
                            f"{BACKEND}/users/login",
                            json={"email": email_val, "password": password_val},
                        )
                    data = r.json()
                    if r.status_code == 200:
                        app.storage.user["token"] = data["token"]
                        app.storage.user["userId"] = data["userId"]
                        ui.navigate.to("/")
                    else:
                        error_msg.set_text(data.get("message", "Erro ao fazer login."))
                except Exception as e:
                    error_msg.set_text(f"Erro de conexão: {e}")

            ui.button("Entrar", on_click=do_login).style(
                "width:100%; background:#16479D; color:white; font-size:1em;"
                " font-weight:bold; padding:0.75em; border-radius:5px; margin-top:0.8em;"
            )

            ui.element("br")
            with ui.element("p").style("margin-top:1.2em; font-size:0.95em; color:#555;"):
                ui.html('Não tem conta? <a href="/register" style="color:#16479D; font-weight:bold;">Cadastre-se</a>')
