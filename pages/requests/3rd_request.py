from dash import html, register_page

import dash_mantine_components as dmc
from dash_iconify import DashIconify

register_page(__name__, path='/requests/3', name='Troisième requête', category_name='Requêtes', title='Requêtes', order=4)

def layout():
    return 'Troisième requête'