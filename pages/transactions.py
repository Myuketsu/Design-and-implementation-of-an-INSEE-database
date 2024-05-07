from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, path='/transactions', name='Transactions', title='Transactions', order=9, icon='grommet-icons:transaction')

def layout():
    return 'C\'est bien vide ici :('