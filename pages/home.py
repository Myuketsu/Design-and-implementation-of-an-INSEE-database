from dash import html, register_page

import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_extensions import Lottie

register_page(__name__, path='/', name='Menu', title='BDA', order=1, icon='bi:house-door-fill')

def layout():
    return 'Page d\'accueil'