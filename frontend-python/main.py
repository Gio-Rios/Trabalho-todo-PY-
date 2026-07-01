"""Ponto de entrada do frontend."""

import os

from nicegui import ui, app

from styles import apply_global_styles
from components.layout.navbar import navbar
from components.layout.footer import footer
from components.pages.home import home_content
from components.pages.auth.login import login_content
from components.pages.auth.register import register_content
from components.pages.pets.add_pet import add_pet_content
from components.pages.pets.my_pets import my_pets_content
from components.pages.pets.my_adoptions import my_adoptions_content
from components.pages.pets.edit_pet import edit_pet_content
from components.pages.user.edit_profile import edit_profile_content

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.add_static_files("/assets", os.path.join(BASE_DIR, "assets"))


def layout(content_fn):
    apply_global_styles()
    navbar()
    content_fn()
    footer()


@ui.page("/")
def index_page():
    layout(home_content)


@ui.page("/login")
def login_page():
    layout(login_content)


@ui.page("/register")
def register_page():
    layout(register_content)


@ui.page("/pets/add")
def add_pet_page():
    layout(add_pet_content)


@ui.page("/pets/mypets")
def my_pets_page():
    layout(my_pets_content)


@ui.page("/pets/myadoptions")
def my_adoptions_page():
    layout(my_adoptions_content)


@ui.page("/pets/edit/{pet_id}")
def edit_pet_page(pet_id: str):
    layout(lambda: edit_pet_content(pet_id))


@ui.page("/users/edit/{user_id}")
def edit_profile_page(user_id: str):
    layout(lambda: edit_profile_content(user_id))


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="0.0.0.0",
        port=3000,
        title="Get A Pet",
        favicon=os.path.join(BASE_DIR, "assets", "img", "logo.png"),
        show=False,
        reload=False,
        storage_secret="getapet_secret_key",
    )
