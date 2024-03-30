from dash import html, register_page

import dash_mantine_components as dmc
from dash_iconify import DashIconify

register_page(__name__, path='/requests/2', name='Seconde requête', category_name='Requêtes', title='Requêtes', order=3)

def layout():
    return 'Seconde requête'