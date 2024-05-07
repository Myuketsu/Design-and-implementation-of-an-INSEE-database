from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, path='/stored_procedure', name='Procédure stockée', title='Procédure stockée', order=4, icon='material-symbols:step')

def layout():
    return 'C\'est bien vide ici :('