"""Página Meus Pets."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def my_pets_content():
    token = app.storage.user.get("token")

    with ui.element("section"):
        if not token:
            ui.html("<h1>Acesso negado</h1>")
            ui.html('<p>Faça <a href="/login" style="color:#16479D; font-weight:bold;">login</a> para ver seus pets.</p>')
            return

        with ui.row().style("align-items:center; justify-content:space-between; margin-bottom:0.5em;"):
            ui.html("<h1>Meus Pets</h1>")
            ui.button("+ Cadastrar novo pet", on_click=lambda: ui.navigate.to("/pets/add")).style(
                "background:#16479D; color:white; font-weight:bold; border-radius:5px; padding:0.5em 1.2em;"
            )

        container = ui.row().style("flex-wrap:wrap; gap:1.5em; padding:1em 0; align-items:flex-start;")

        async def load_my_pets():
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(
                        f"{BACKEND}/pets/mypets",
                        headers={"Authorization": f"Bearer {token}"},
                    )
                pets = r.json().get("pets", [])
                container.clear()

                if not pets:
                    with container:
                        ui.label("Você ainda não cadastrou nenhum pet.").style("color:#777; font-size:1.05em;")
                    return

                with container:
                    for pet in pets:
                        pet_id = pet["_id"]
                        with ui.card().style(
                            "width:260px; border-radius:10px; overflow:hidden;"
                            " border:1px solid #e0e0e0; box-shadow:0 2px 8px rgba(0,0,0,0.08);"
                        ):
                            if pet.get("images"):
                                ui.image(f"{BACKEND}/images/pets/{pet['images'][0]}").style(
                                    "width:100%; height:175px; object-fit:cover;"
                                )

                            with ui.element("div").style("padding:0.8em 1em;"):
                                ui.label(pet["name"]).style(
                                    "font-size:1.1em; font-weight:bold; color:#16479D;"
                                )

                                is_available = pet.get("available", True)
                                status_text = "Disponível" if is_available else "Adoção concluída"
                                status_color = "#2e7d32" if is_available else "#888"
                                ui.label(status_text).style(
                                    f"color:{status_color}; font-size:0.85em; font-weight:bold; margin-top:0.2em;"
                                )

                                if pet.get("adopter") and is_available:
                                    ui.label(f"Interessado: {pet['adopter']['name']}").style(
                                        "color:#555; font-size:0.85em;"
                                    )

                                with ui.row().style("margin-top:0.8em; gap:0.4em; flex-wrap:wrap;"):
                                    ui.button(
                                        "Editar",
                                        on_click=lambda pid=pet_id: ui.navigate.to(f"/pets/edit/{pid}"),
                                    ).style(
                                        "background:#16479D; color:white; font-size:0.8em;"
                                        " border-radius:4px; padding:0.4em 0.9em;"
                                    )

                                    async def delete_pet(pid=pet_id):
                                        try:
                                            async with httpx.AsyncClient() as client:
                                                r = await client.delete(
                                                    f"{BACKEND}/pets/{pid}",
                                                    headers={"Authorization": f"Bearer {token}"},
                                                )
                                            if r.status_code == 200:
                                                ui.notify("Pet removido!", type="positive")
                                                await load_my_pets()
                                            else:
                                                ui.notify(
                                                    r.json().get("message", "Erro ao remover."),
                                                    type="negative",
                                                )
                                        except Exception as e:
                                            ui.notify(f"Erro: {e}", type="negative")

                                    ui.button("Excluir", on_click=delete_pet).style(
                                        "background:#c62828; color:white; font-size:0.8em;"
                                        " border-radius:4px; padding:0.4em 0.9em;"
                                    )

                                    if pet.get("adopter") and is_available:
                                        async def conclude(pid=pet_id):
                                            try:
                                                async with httpx.AsyncClient() as client:
                                                    r = await client.patch(
                                                        f"{BACKEND}/pets/conclude/{pid}",
                                                        headers={"Authorization": f"Bearer {token}"},
                                                    )
                                                data = r.json()
                                                if r.status_code == 200:
                                                    ui.notify(data["message"], type="positive")
                                                    await load_my_pets()
                                                else:
                                                    ui.notify(
                                                        data.get("message", "Erro."),
                                                        type="negative",
                                                    )
                                            except Exception as e:
                                                ui.notify(f"Erro: {e}", type="negative")

                                        ui.button("Concluir adoção", on_click=conclude).style(
                                            "background:#388e3c; color:white; font-size:0.8em;"
                                            " border-radius:4px; padding:0.4em 0.9em;"
                                        )

            except Exception as e:
                ui.notify(f"Erro ao carregar pets: {e}", type="negative")

        ui.timer(0.05, load_my_pets, once=True)
