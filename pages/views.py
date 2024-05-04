from dash import html, register_page
from dash import callback, Input, Output
import dash_mantine_components as dmc

from collections import namedtuple

from data.db_connector import execute_sql
from data.data_processing import extract_from_file
from view.figure import create_table

register_page(__name__, path='/views', name='Vues', title='Vues', order=3, icon='carbon:data-view')

View = namedtuple('Request', ['view_sql', 'query'])

VIEWS: list[View] = [
    View(substr, f'SELECT * FROM {substr.split(' ')[2]};')
    for substr in extract_from_file('./data/sql/create_views.sql', 'CREATE VIEW', ';')
]

# --- LAYOUT ---

def layout():
    return html.Div(
        [
            view_selector(),
            view_body()
        ],
        id='views_layout'
    )

def view_selector() -> html.Div:
    data = [
        {'value': index, 'label': f'Vue {index + 1}'} for index in range(len(VIEWS))
    ]
    return html.Div(
        [
            dmc.Select(
                label=dmc.Text('Selection de la vue', weight=700),
                value=0,
                data=data,
                id='view_selector'
            ),
            html.Div(className='separator'),
            html.Div(
                [
                    dmc.Title('Code SQL associé à la création de la vue', order=6),
                    dmc.Prism(
                        VIEWS[0].view_sql,
                        language='sql',
                        withLineNumbers=True,
                        id='view_selector_SQL_viewer'
                    )
                ],
                id='view_selector_SQL'
            )
        ],
        id='view_selector_body'
    )

def view_body() -> html.Div:
    return html.Div(
        [
            dmc.Title('Résultat de la vue sélectionnée', order=6),
            dmc.Table(
                children='create_table(execute_sql(VIEWS[0].query))', #TODO
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=False,
                id='view_body_table'
            )
        ],
        id='view_body'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('view_selector_SQL_viewer', 'children'),
        Output('view_body_table', 'children')
    ],
    [
        Input('view_selector', 'value')
    ])
def update_reconstructed_curve(in_request: int) -> tuple:
    sql_query = VIEWS[in_request].view_sql
    table = 'create_table(execute_sql(VIEWS[in_request].query))' #TODO
    return sql_query, table