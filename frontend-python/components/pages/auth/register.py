"""Página Register."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def register_content():
    with ui.element("section"):
        with ui.element("div").style("max-width:460px; margin:2em auto;"):
            ui.label("Cadastro").style(
                "font-size:2.1em; font-weight:bold; color:#16479D; margin-bottom:1em; display:block;"
            )

            name_input = ui.input(label="Nome", placeholder="Digite o seu nome").style("width:100%;")
            email_input = ui.input(label="E-mail", placeholder="Digite o seu e-mail").style("width:100%;")
            phone_input = ui.input(label="Telefone", placeholder="Digite o seu telefone").style("width:100%;")
            password_input = ui.input(
                label="Senha",
                placeholder="Digite a sua senha",
                password=True,
                password_toggle_button=True,
            ).style("width:100%;")
            confirm_input = ui.input(
                label="Confirmação de Senha",
                placeholder="Confirme a sua senha",
                password=True,
                password_toggle_button=True,
            ).style("width:100%;")

            error_msg = ui.label("").style("color:#d32f2f; font-size:0.92em; margin-top:0.3em;")

            async def do_register():
                error_msg.set_text("")
                try:
                    async with httpx.AsyncClient() as client:
                        r = await client.post(
                            f"{BACKEND}/users/register",
                            json={
                                "name": name_input.value.strip(),
                                "email": email_input.value.strip(),
                                "phone": phone_input.value.strip(),
                                "password": password_input.value,
                                "confirmpassword": confirm_input.value,
                            },
                        )
                    data = r.json()
                    if r.status_code == 200:
                        app.storage.user["token"] = data["token"]
                        app.storage.user["userId"] = data["userId"]
                        ui.navigate.to("/")
                    else:
                        error_msg.set_text(data.get("message", "Erro ao cadastrar."))
                except Exception as e:
                    error_msg.set_text(f"Erro de conexão: {e}")

            ui.button("Cadastrar", on_click=do_register).style(
                "width:100%; background:#16479D; color:white; font-size:1em;"
                " font-weight:bold; padding:0.75em; border-radius:5px; margin-top:0.8em;"
            )

            ui.element("br")
            with ui.element("p").style("margin-top:1.2em; font-size:0.95em; color:#555;"):
                ui.html('Já tem conta? <a href="/login" style="color:#16479D; font-weight:bold;">Entre aqui</a>')
