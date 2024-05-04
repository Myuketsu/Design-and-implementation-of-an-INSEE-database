from dash import register_page
from dash.dcc import Markdown

register_page(__name__, path='/', name='Menu', title='BDA', order=1, icon='bi:house-door-fill')

def layout():
    with open('./README.md', 'r') as readme:
        return Markdown(
            readme.read(),
            id='home_readme'
        )