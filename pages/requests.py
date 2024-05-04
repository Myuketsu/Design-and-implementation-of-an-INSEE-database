from dash import html, register_page
from dash import callback, Input, Output
import dash_mantine_components as dmc

from collections import namedtuple

from data.db_connector import execute_sql
from view.figure import create_table

register_page(__name__, path='/requests', name='Requêtes', title='Requêtes', order=2, icon='bi:database-down')

Request = namedtuple('Request', ['query', 'vars'])

REQUESTS: list[Request] = [
    Request('SELECT * FROM region;', tuple()),
    Request('SELECT * FROM departement;', tuple()),
    Request('SELECT * FROM commune;', tuple())
]

# --- LAYOUT ---

def layout():
    return html.Div(
        [
            request_selector(),
            request_body()
        ],
        id='requests_layout'
    )

def request_selector() -> html.Div:
    data = [
        {'value': index, 'label': f'Requête {index + 1}'} for index in range(len(REQUESTS))
    ]
    return html.Div(
        [
            dmc.Select(
                label=dmc.Text('Selection de la requête', weight=700),
                value=0,
                data=data,
                id='request_selector'
            ),
            html.Div(className='separator'),
            html.Div(
                [
                    dmc.Title('Contenu de la requête SQL', order=6),
                    dmc.Prism(
                        REQUESTS[0].query % REQUESTS[0].vars,
                        language='sql',
                        withLineNumbers=True,
                        id='request_selector_SQL_viewer'
                    )
                ],
                id='request_selector_SQL'
            )
        ],
        id='request_selector_body'
    )

def request_body() -> html.Div:
    return html.Div(
        [
            dmc.Title('Résultat de la requête sélectionnée', order=6),
            dmc.Table(
                children=create_table(execute_sql(*REQUESTS[0])),
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=False,
                id='request_body_table'
            )
        ],
        id='request_body'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('request_selector_SQL_viewer', 'children'),
        Output('request_body_table', 'children')
    ],
    [
        Input('request_selector', 'value')
    ])
def update_reconstructed_curve(in_request: int) -> tuple:
    sql_query = REQUESTS[in_request].query % REQUESTS[in_request].vars
    table = create_table(execute_sql(*REQUESTS[in_request]))
    return sql_query, table