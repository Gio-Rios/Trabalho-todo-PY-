"""Página Minhas Adoções."""

import httpx
from nicegui import ui, app

BACKEND = "http://localhost:5000"


def my_adoptions_content():
    token = app.storage.user.get("token")

    with ui.element("section"):
        if not token:
            ui.html("<h1>Acesso negado</h1>")
            ui.html('<p>Faça <a href="/login" style="color:#16479D; font-weight:bold;">login</a> para ver suas adoções.</p>')
            return

        ui.html("<h1>Minhas Adoções</h1>")
        container = ui.row().style("flex-wrap:wrap; gap:1.5em; padding:1em 0; align-items:flex-start;")

        async def load():
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(
                        f"{BACKEND}/pets/myadoptions",
                        headers={"Authorization": f"Bearer {token}"},
                    )
                pets = r.json().get("pets", [])
                container.clear()

                if not pets:
                    with container:
                        ui.label("Você não tem nenhuma adoção agendada.").style("color:#777; font-size:1.05em;")
                    return

                with container:
                    for pet in pets:
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
                                status_text = "Visita agendada ✓" if is_available else "Adoção concluída"
                                status_color = "#1565c0" if is_available else "#388e3c"
                                ui.label(status_text).style(
                                    f"color:{status_color}; font-size:0.85em; font-weight:bold; margin-top:0.2em;"
                                )

                                ui.element("hr").style("margin:0.6em 0; border-color:#eee;")
                                ui.label("Responsável pelo pet:").style("color:#555; font-size:0.85em; font-weight:bold;")
                                ui.label(pet["user"]["name"]).style("color:#333; font-size:0.95em;")
                                ui.label(f"Tel: {pet['user']['phone']}").style("color:#555; font-size:0.85em;")

            except Exception as e:
                ui.notify(f"Erro: {e}", type="negative")

        ui.timer(0.05, load, once=True)
