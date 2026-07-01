"""Página Editar Pet."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def edit_pet_content(pet_id: str):
    token = app.storage.user.get("token")

    with ui.element("section"):
        if not token:
            ui.html("<h1>Acesso negado</h1>")
            return

        with ui.element("div").style("max-width:520px; margin:0 auto;"):
            ui.html("<h1>Editar Pet</h1>")

            name_input = ui.input("Nome do pet").style("width:100%;")
            age_input = ui.input("Idade").style("width:100%;")
            weight_input = ui.input("Peso (kg)").style("width:100%;")
            color_input = ui.input("Cor").style("width:100%;")
            avail_check = ui.checkbox("Disponível para adoção", value=True)

            ui.label("Novas imagens (opcional — substitui as atuais)").style(
                "color:#555; font-size:0.9em; margin-top:0.5em; display:block;"
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
                label="Selecione novas imagens",
            ).style("width:100%; margin-bottom:0.5em;")

            error_msg = ui.label("").style("color:#d32f2f; font-size:0.9em;")

            async def load_pet():
                try:
                    async with httpx.AsyncClient() as client:
                        r = await client.get(
                            f"{BACKEND}/pets/mypets",
                            headers={"Authorization": f"Bearer {token}"},
                        )
                    pets = r.json().get("pets", [])
                    pet = next((p for p in pets if p["_id"] == pet_id), None)
                    if pet:
                        name_input.set_value(pet["name"])
                        age_input.set_value(str(pet["age"]))
                        weight_input.set_value(str(pet["weight"]))
                        color_input.set_value(pet["color"])
                        avail_check.set_value(bool(pet.get("available", True)))
                    else:
                        error_msg.set_text("Pet não encontrado.")
                except Exception as e:
                    error_msg.set_text(f"Erro ao carregar pet: {e}")

            ui.timer(0.05, load_pet, once=True)

            async def do_edit():
                error_msg.set_text("")
                if not name_input.value or not age_input.value or not weight_input.value or not color_input.value:
                    error_msg.set_text("Preencha todos os campos!")
                    return
                try:
                    form_data = {
                        "name": name_input.value,
                        "age": age_input.value,
                        "weight": weight_input.value,
                        "color": color_input.value,
                        "available": str(avail_check.value).lower(),
                    }
                    async with httpx.AsyncClient() as client:
                        if uploaded_files:
                            files = [
                                ("images", (f["name"], f["content"], f["type"]))
                                for f in uploaded_files
                            ]
                            r = await client.patch(
                                f"{BACKEND}/pets/{pet_id}",
                                data=form_data,
                                files=files,
                                headers={"Authorization": f"Bearer {token}"},
                            )
                        else:
                            r = await client.patch(
                                f"{BACKEND}/pets/{pet_id}",
                                data=form_data,
                                headers={"Authorization": f"Bearer {token}"},
                            )
                    data = r.json()
                    if r.status_code == 200:
                        ui.notify("Pet atualizado com sucesso!", type="positive")
                        ui.navigate.to("/pets/mypets")
                    else:
                        error_msg.set_text(data.get("message", "Erro ao atualizar."))
                except Exception as e:
                    error_msg.set_text(f"Erro: {e}")

            ui.button("Salvar alterações", on_click=do_edit).style(
                "background:#16479D; color:white; font-weight:bold; border-radius:5px;"
                " padding:0.7em 2em; margin-top:0.5em;"
            )
