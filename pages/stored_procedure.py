from dash import html, register_page
import dash_mantine_components as dmc

from data.data_processing import SQL_PATH, get_file_content

register_page(__name__, path='/stored_procedure', name='Procédure stockée', title='Procédure stockée', order=4, icon='material-symbols:step')

def layout():
    return html.Div(
        [
            dmc.Prism(
                get_file_content(f'{SQL_PATH}procedure.sql'),
                language='sql',
                withLineNumbers=True
            )
        ],
        id='procedure_layout',
        className='layout_code_highlight'
    )