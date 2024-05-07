from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, path='/execution_plan', name='Plan d\'exécution', title='Plan d\'exécution', order=7, category_name='Plan d\'exécution')

def layout():
    return 'C\'est bien vide ici :('