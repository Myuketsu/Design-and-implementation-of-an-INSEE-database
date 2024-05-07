from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, path='/triggers', name='Triggers', title='Triggers', order=5, category_name='Triggers')

def layout():
    with open('./data/sql/triggers.sql', 'r', encoding='utf-8') as triggers:
        return html.Div(
            [
                dmc.Prism(
                    triggers.read(),
                    language='sql',
                    withLineNumbers=True,
                    id='triggers_SQL_viewer'
                )
            ],
            id='triggers_layout'
        )