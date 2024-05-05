from dash import html, register_page
from dash import callback, Input, Output
from dash.dash_table import DataTable
import dash_mantine_components as dmc

from collections import namedtuple

from data.db_connector import execute_sql
from data.data_processing import load_query

register_page(__name__, path='/requests', name='Requêtes', title='Requêtes', order=2, icon='bi:database-down')

query_file = load_query('./data/sql/requests.toml')

Request = namedtuple('Request', ['title', 'desc', 'query'])
REQUESTS: list[Request] = [
    Request(item.get('title'), item.get('desc'), item.get('query'))
    for item in query_file.values()
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
        {'value': index, 'label': request.title} for index, request in enumerate(REQUESTS)
    ]
    return html.Div(
        [
            html.Div(
                [
                    dmc.Select(
                        label=dmc.Text('Selection de la requête', weight=700),
                        value=0,
                        data=data,
                        id='request_selector'
                    )
                ],
                id='request_selector_box'
            ),
            html.Div(className='separator'),
            html.Div(
                [
                    dmc.Title('Contenu de la requête SQL', order=6),
                    dmc.Prism(
                        REQUESTS[0].query,
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
    df = execute_sql(REQUESTS[0].query)
    return html.Div(
        [
            dmc.Title(REQUESTS[0].desc, order=6, id='request_body_table_title'),
            DataTable(
                data=df.to_dict('records'),
                columns=[{'id': col, 'name': col} for col in df.columns],
                page_size=19,
                style_table={
                    'border-left': '1px solid rgb(233, 236, 239)',
                    'border-right': '1px solid rgb(233, 236, 239)'
                },
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                id='request_body_table'
            )
        ],
        id='request_body'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('request_selector_SQL_viewer', 'children'),
        Output('request_body_table', 'data'),
        Output('request_body_table', 'columns'),
        Output('request_body_table_title', 'children')
    ],
    [
        Input('request_selector', 'value')
    ])
def update_reconstructed_curve(in_request: int) -> tuple:
    sql_query = REQUESTS[in_request].query

    df = execute_sql(REQUESTS[in_request].query)
    data = df.to_dict('records')
    columns = [{'id': col, 'name': col} for col in df.columns]

    desc_table = REQUESTS[in_request].desc

    return sql_query, data, columns, desc_table