from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, path='/triggers_suite', name='Suite', title='Triggers suite', order=6, category_name='Triggers')

def layout():
    return 'C\'est bien vide ici :('