"""Página Cadastrar Pet."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def add_pet_content():
    token = app.storage.user.get("token")

    with ui.element("section"):
        if not token:
            ui.html("<h1>Acesso negado</h1>")
            ui.html('<p>Faça <a href="/login" style="color:#16479D; font-weight:bold;">login</a> para cadastrar um pet.</p>')
            return

        with ui.element("div").style("max-width:520px; margin:0 auto;"):
            ui.html("<h1>Cadastrar Pet</h1>")

            name_input = ui.input("Nome do pet").style("width:100%;")
            age_input = ui.input("Idade").style("width:100%;")
            weight_input = ui.input("Peso (kg)").style("width:100%;")
            color_input = ui.input("Cor").style("width:100%;")

            ui.label("Imagens do pet (PNG ou JPG)").style(
                "font-weight:bold; color:#16479D; margin-top:0.5em; display:block;"
            )

            uploaded_files = []

            async def on_upload(e):
                data = await e.file.read()
                uploaded_files.append({
                    "name": e.file.name,
                    "content": data,
                    "type": e.file.content_type,
                })

            ui.upload(
                multiple=True,
                on_upload=on_upload,
                auto_upload=True,
                label="Selecione as imagens",
            ).style("width:100%; margin-bottom:0.5em;")

            error_msg = ui.label("").style("color:#d32f2f; font-size:0.9em; margin-bottom:0.5em;")

            async def do_add():
                error_msg.set_text("")
                if not name_input.value or not age_input.value or not weight_input.value or not color_input.value:
                    error_msg.set_text("Preencha todos os campos!")
                    return
                if not uploaded_files:
                    error_msg.set_text("Envie ao menos uma imagem!")
                    return
                try:
                    files = [
                        ("images", (f["name"], f["content"], f["type"]))
                        for f in uploaded_files
                    ]
                    async with httpx.AsyncClient() as client:
                        r = await client.post(
                            f"{BACKEND}/pets/create",
                            data={
                                "name": name_input.value,
                                "age": age_input.value,
                                "weight": weight_input.value,
                                "color": color_input.value,
                            },
                            files=files,
                            headers={"Authorization": f"Bearer {token}"},
                        )
                    data = r.json()
                    if r.status_code in (200, 201, 301):
                        ui.notify("Pet cadastrado com sucesso!", type="positive")
                        ui.navigate.to("/pets/mypets")
                    else:
                        error_msg.set_text(data.get("message", "Erro ao cadastrar pet."))
                except Exception as e:
                    error_msg.set_text(f"Erro: {e}")

            ui.button("Cadastrar Pet", on_click=do_add).style(
                "background:#16479D; color:white; font-weight:bold; border-radius:5px;"
                " padding:0.7em 2em; margin-top:0.5em;"
            )
