"""Navbar (equivalente a src/components/layout/Navbar.js).

No React era um componente que renderizava o logo, o título e os links
de navegação (react-router Link). Aqui é uma função Python que monta os
mesmos elementos com ui.link (navegação client-side do NiceGUI).
"""

from nicegui import ui, app


def navbar():
    token = app.storage.user.get("token")
    user_id = app.storage.user.get("userId")

    with ui.element("nav"):
        with ui.element("div").classes("brand"):
            ui.image("/assets/img/logo.png").classes("brand-logo")
            ui.html('<a href="/" style="text-decoration:none"><h2 style="color:#16479D">Get A Pet</h2></a>')
        with ui.element("ul"):
            with ui.element("li"):
                ui.link("Adotar", "/")
            if token:
                with ui.element("li"):
                    ui.link("Cadastrar Pet", "/pets/add")
                with ui.element("li"):
                    ui.link("Meus Pets", "/pets/mypets")
                with ui.element("li"):
                    ui.link("Minhas Adoções", "/pets/myadoptions")
                with ui.element("li"):
                    ui.link("Editar Perfil", f"/users/edit/{user_id}")
                with ui.element("li"):
                    async def do_logout():
                        app.storage.user.clear()
                        ui.navigate.to("/")
                    ui.button("Sair", on_click=do_logout).style(
                        "background:none; border:none; color:#16479D; font-weight:bold;"
                        " cursor:pointer; font-size:1em; padding:0; box-shadow:none;"
                    )
            else:
                with ui.element("li"):
                    ui.link("Entrar", "/login")
                with ui.element("li"):
                    ui.link("Cadastrar", "/register")
