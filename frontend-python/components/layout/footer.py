"""Footer (equivalente a src/components/layout/Footer.js)."""

from nicegui import ui


def footer():
    with ui.element("footer"):
        ui.html('<p><span class="bold">Get A Pet</span> &copy; 2025</p>')
