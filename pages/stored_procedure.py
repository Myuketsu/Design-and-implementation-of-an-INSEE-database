from dash import html, register_page
import dash_mantine_components as dmc

register_page(__name__, path='/stored_procedure', name='Procédure stockée', title='Procédure stockée', order=4, icon='material-symbols:step')

def layout():
    with open('./data/sql/procedure.sql', 'r', encoding='utf-8') as triggers:
        return html.Div(
            [
                dmc.Prism(
                    triggers.read(),
                    language='sql',
                    withLineNumbers=True
                )
            ],
            id='procedure_layout',
            className='layout_code_highlight'
        )