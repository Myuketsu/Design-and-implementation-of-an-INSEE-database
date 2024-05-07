from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, path='/execution_plan_and_index', name='Index', title='Plan d\'exécution et Index', order=8, category_name='Plan d\'exécution')

def layout():
    return 'C\'est bien vide ici :('