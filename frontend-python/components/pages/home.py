"""Página Home — lista todos os pets disponíveis para adoção."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def home_content():
    with ui.element("section"):
        ui.html("<h1>Pets disponíveis para adoção</h1>")

        loading = ui.label("Carregando pets...").style("color:#777; font-size:1.05em;")
        container = ui.row().style("flex-wrap:wrap; gap:1.5em; padding:1em 0; align-items:flex-start;")

        def show_dialog(pet):
            token = app.storage.user.get("token")
            user_id = app.storage.user.get("userId")
            is_owner = bool(user_id and str(pet["user"].get("_id")) == str(user_id))

            with ui.dialog() as dialog, ui.card().style("width:min(420px, 90vw); max-width:540px; padding:1.2em;"):
                if pet.get("images"):
                    ui.image(f"{BACKEND}/images/pets/{pet['images'][0]}").style(
                        "width:100%; max-height:260px; object-fit:cover; border-radius:8px;"
                    )
                ui.label(pet["name"]).style(
                    "font-size:1.4em; font-weight:bold; color:#16479D; margin-top:0.8em;"
                )
                with ui.element("div").style("margin:0.5em 0; display:flex; flex-direction:column; gap:0.25em;"):
                    ui.label(f"Idade: {pet['age']}").style("color:#555;")
                    ui.label(f"Peso: {pet['weight']} kg").style("color:#555;")
                    ui.label(f"Cor: {pet['color']}").style("color:#555;")

                ui.label("Responsável:").style("font-weight:bold; color:#16479D; margin-top:0.7em;")
                with ui.row().style("align-items:center; gap:0.6em; margin-bottom:0.3em;"):
                    if pet["user"].get("image"):
                        ui.image(f"{BACKEND}/images/users/{pet['user']['image']}").style(
                            "width:38px; height:38px; border-radius:50%; object-fit:cover;"
                        )
                    ui.label(pet["user"]["name"]).style("color:#333;")
                ui.label(f"Telefone: {pet['user']['phone']}").style("color:#555;")

                notice = ui.label("").style("color:#d32f2f; font-size:0.9em; margin-top:0.4em;")

                with ui.row().style("margin-top:1em; gap:0.6em;"):
                    if token and not is_owner:
                        async def agendar(p=pet):
                            t = app.storage.user.get("token")
                            try:
                                async with httpx.AsyncClient() as client:
                                    r = await client.patch(
                                        f"{BACKEND}/pets/schedule/{p['_id']}",
                                        headers={"Authorization": f"Bearer {t}"},
                                    )
                                data = r.json()
                                if r.status_code == 200:
                                    dialog.close()
                                    ui.notify(data["message"], type="positive", timeout=5000)
                                else:
                                    notice.set_text(data.get("message", "Erro ao agendar."))
                            except Exception as e:
                                notice.set_text(f"Erro: {e}")

                        ui.button("Agendar visita", on_click=agendar).style(
                            "background:#16479D; color:white; font-weight:bold; border-radius:5px;"
                        )
                    elif not token:
                        ui.label("Faça login para agendar uma visita.").style("color:#777; font-size:0.9em;")

                    ui.button("Fechar", on_click=dialog.close).style(
                        "background:#eee; color:#444; border-radius:5px;"
                    )
            dialog.open()

        async def load_pets():
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(f"{BACKEND}/pets/")
                pets = r.json().get("pets", [])
                available = [p for p in pets if p.get("available")]

                loading.set_visibility(False)
                container.clear()

                if not available:
                    with container:
                        ui.label("Nenhum pet disponível para adoção no momento.").style("color:#777; font-size:1.05em;")
                    return

                with container:
                    for pet in available:
                        with ui.card().style(
                            "flex:1 1 220px; max-width:280px; min-width:200px;"
                            " border-radius:10px; overflow:hidden;"
                            " border:1px solid #e0e0e0; box-shadow:0 2px 8px rgba(0,0,0,0.08);"
                        ):
                            if pet.get("images"):
                                ui.image(f"{BACKEND}/images/pets/{pet['images'][0]}").style(
                                    "width:100%; height:175px; object-fit:cover;"
                                )
                            else:
                                ui.label("🐾").style(
                                    "font-size:3em; text-align:center; padding:1em;"
                                    " background:#f5f5f5; display:block; width:100%;"
                                )

                            with ui.element("div").style("padding:0.8em 1em;"):
                                ui.label(pet["name"]).style(
                                    "font-size:1.1em; font-weight:bold; color:#16479D; margin-bottom:0.3em;"
                                )
                                ui.label(f"Idade: {pet['age']}").style("color:#555; font-size:0.9em;")
                                ui.label(f"Peso: {pet['weight']} kg").style("color:#555; font-size:0.9em;")
                                ui.label(f"Cor: {pet['color']}").style("color:#555; font-size:0.9em;")

                                def make_handler(p):
                                    def handler():
                                        show_dialog(p)
                                    return handler

                                ui.button("Ver mais", on_click=make_handler(pet)).style(
                                    "background:#16479D; color:white; font-weight:bold; border-radius:5px;"
                                    " font-size:0.9em; width:100%; margin-top:0.7em;"
                                )

            except Exception as e:
                loading.set_text(f"Erro ao carregar pets: {e}")
                loading.style("color:#d32f2f;")

        ui.timer(0.05, load_pets, once=True)
