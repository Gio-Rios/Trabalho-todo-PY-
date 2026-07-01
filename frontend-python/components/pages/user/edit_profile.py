"""Página Editar Perfil."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def edit_profile_content(user_id: str):
    token = app.storage.user.get("token")
    stored_id = app.storage.user.get("userId")

    with ui.element("section"):
        if not token or stored_id != user_id:
            ui.html("<h1>Acesso negado</h1>")
            return

        with ui.element("div").style("max-width:520px; margin:0 auto;"):
            ui.html("<h1>Editar Perfil</h1>")

            avatar_container = ui.element("div").style("margin-bottom:1em;")

            name_input = ui.input("Nome").style("width:100%;")
            email_input = ui.input("E-mail").style("width:100%;")
            phone_input = ui.input("Telefone").style("width:100%;")
            password_input = ui.input(
                "Nova senha (deixe vazio para manter)",
                password=True,
                password_toggle_button=True,
            ).style("width:100%;")
            confirm_input = ui.input(
                "Confirmar nova senha",
                password=True,
                password_toggle_button=True,
            ).style("width:100%;")

            ui.label("Foto de perfil (opcional)").style(
                "color:#555; font-size:0.9em; margin-top:0.5em; display:block;"
            )

            uploaded_image = []

            async def on_upload(e):
                data = await e.file.read()
                uploaded_image.clear()
                uploaded_image.append({
                    "name": e.file.name,
                    "content": data,
                    "type": e.file.content_type,
                })

            ui.upload(
                on_upload=on_upload,
                auto_upload=True,
                label="Selecione uma foto",
            ).style("width:100%; margin-bottom:0.5em;")

            error_msg = ui.label("").style("color:#d32f2f; font-size:0.9em;")

            async def load_user():
                try:
                    async with httpx.AsyncClient() as client:
                        r = await client.get(f"{BACKEND}/users/{user_id}")
                    user = r.json().get("user", {})
                    name_input.set_value(user.get("name", ""))
                    email_input.set_value(user.get("email", ""))
                    phone_input.set_value(user.get("phone", ""))
                    if user.get("image"):
                        with avatar_container:
                            ui.image(f"{BACKEND}/images/users/{user['image']}").style(
                                "width:80px; height:80px; border-radius:50%; object-fit:cover;"
                                " border:3px solid #16479D;"
                            )
                except Exception as e:
                    error_msg.set_text(f"Erro ao carregar dados: {e}")

            ui.timer(0.05, load_user, once=True)

            async def do_edit():
                error_msg.set_text("")
                try:
                    form_data = {
                        "name": name_input.value,
                        "email": email_input.value,
                        "phone": phone_input.value,
                        "password": password_input.value,
                        "confirmpassword": confirm_input.value,
                    }
                    async with httpx.AsyncClient() as client:
                        if uploaded_image:
                            img = uploaded_image[0]
                            r = await client.patch(
                                f"{BACKEND}/users/edit/{user_id}",
                                data=form_data,
                                files={"image": (img["name"], img["content"], img["type"])},
                                headers={"Authorization": f"Bearer {token}"},
                            )
                        else:
                            r = await client.patch(
                                f"{BACKEND}/users/edit/{user_id}",
                                data=form_data,
                                headers={"Authorization": f"Bearer {token}"},
                            )
                    data = r.json()
                    if r.status_code == 200:
                        ui.notify("Perfil atualizado com sucesso!", type="positive")
                    else:
                        error_msg.set_text(data.get("message", "Erro ao atualizar."))
                except Exception as e:
                    error_msg.set_text(f"Erro: {e}")

            ui.button("Salvar alterações", on_click=do_edit).style(
                "background:#16479D; color:white; font-weight:bold; border-radius:5px;"
                " padding:0.7em 2em; margin-top:0.5em;"
            )
