"""Estilos globais (equivalente a src/index.css).

No React o CSS ficava em index.css. No NiceGUI injetamos o mesmo CSS
global em Python via ui.add_head_html, mantendo o reset e as cores.
"""

from nicegui import ui

GLOBAL_CSS = """
<style>
  * {
    padding: 0;
    margin: 0;
    font-family: Helvetica;
    box-sizing: border-box;
  }

  html, body {
    min-height: 100vh;
    background: linear-gradient(180deg, #eef3fb 0%, #f8fafc 45%, #eef3fb 100%);
  }

  .nicegui-content {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  h1 {
    color: #16479D;
    margin-bottom: 1em;
    font-size: 2.1em;
  }

  .bold {
    font-weight: bold;
    color: #16479D;
  }

  /* Navbar */
  nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8em 2em;
    background-color: #fff;
    border-bottom: 1px solid #eee;
    box-shadow: 0 2px 6px rgba(22, 71, 157, 0.06);
  }
  nav .brand {
    display: flex;
    align-items: center;
    gap: 0.6em;
    text-decoration: none;
  }
  nav .brand img {
    width: 48px;
    height: 48px;
    object-fit: contain;
  }
  nav ul {
    display: flex;
    list-style: none;
    gap: 1.5em;
  }
  nav ul a {
    text-decoration: none;
    color: #16479D;
    font-weight: bold;
  }

  /* Conteúdo das páginas */
  section {
    flex: 1;
    padding: 2em;
  }

  /* Footer */
  footer {
    padding: 1.2em 2em;
    text-align: center;
    border-top: 1px solid #eee;
    background-color: #fff;
  }

  /* Pet cards grid */
  .pets-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5em;
    padding: 1em 0;
  }

  .pet-card {
    width: 240px;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    overflow: hidden;
    background: #fff;
  }

  .pet-card img {
    width: 100%;
    height: 175px;
    object-fit: cover;
  }

  .pet-card-body {
    padding: 0.8em 1em;
  }

  .pet-card-name {
    font-size: 1.15em;
    font-weight: bold;
    color: #16479D;
    margin-bottom: 0.4em;
  }

  .pet-card-info {
    color: #555;
    font-size: 0.9em;
    margin-bottom: 0.2em;
  }

  .pet-card-btn {
    display: block;
    margin-top: 0.8em;
    padding: 0.5em 1em;
    background: #16479D;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9em;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
  }

  /* Formulários de auth */
  .form-container {
    max-width: 460px;
    margin: 2em auto;
  }

  .form-container h1 {
    margin-bottom: 1.2em;
  }

  .form-field {
    width: 100%;
    padding: 0.7em 0.9em;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1em;
    margin-bottom: 1em;
    outline: none;
  }

  .form-field:focus {
    border-color: #16479D;
  }

  .form-btn {
    width: 100%;
    padding: 0.75em;
    background: #16479D;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    font-weight: bold;
    cursor: pointer;
    margin-top: 0.5em;
  }

  .form-btn:hover {
    background: #0f3480;
  }

  .form-error {
    color: #d32f2f;
    font-size: 0.92em;
    margin-bottom: 0.8em;
  }

  .form-link {
    margin-top: 1.2em;
    font-size: 0.95em;
    color: #555;
  }

  .form-link a {
    color: #16479D;
    font-weight: bold;
    text-decoration: none;
  }

  .empty-msg {
    color: #777;
    font-size: 1.05em;
    padding: 2em 0;
  }

  .page-loading {
    padding: 3em 0;
    text-align: center;
    color: #777;
  }
</style>
"""


def apply_global_styles():
    ui.add_head_html(GLOBAL_CSS)
