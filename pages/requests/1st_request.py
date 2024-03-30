from dash import html, register_page

import dash_mantine_components as dmc
from dash_iconify import DashIconify

register_page(__name__, path='/requests/1', name='Première requête', category_name='Requêtes', title='Requêtes', order=2)

def layout():
    return 'Première requête'