from dash import html, register_page
from dash import callback, Input, Output
from dash.dash_table import DataTable
import dash_mantine_components as dmc

from collections import namedtuple

from data.db_connector import execute_sql
from data.data_processing import load_query
from view.figure import create_table

register_page(__name__, path='/views', name='Vues', title='Vues', order=3, icon='carbon:data-view')

query_file = load_query('./data/sql/create_views.toml')

View = namedtuple('View', ['view_sql', 'query'])
VIEWS: list[View] = [
    View(item.get('view_sql'), item.get('query'))
    for item in query_file.values()
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
            html.Div(
                dmc.Select(
                    label=dmc.Text('Selection de la vue', weight=700),
                    value=0,
                    data=data,
                    id='view_selector'
                ),
                id='view_selector_box'
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
    df = execute_sql(VIEWS[0].query)
    return html.Div(
        [
            dmc.Title('Résultat de la vue sélectionnée', order=6),
            DataTable(
                data=df.to_dict('records'),
                columns=[{'id': col, 'name': col} for col in df.columns],
                page_size=21,
                style_table={
                    'border-left': '1px solid rgb(233, 236, 239)',
                    'border-right': '1px solid rgb(233, 236, 239)'
                },
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                id='view_body_table'
            )
        ],
        id='view_body'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('view_selector_SQL_viewer', 'children'),
        Output('view_body_table', 'data'),
        Output('view_body_table', 'columns')
    ],
    [
        Input('view_selector', 'value')
    ])
def update_reconstructed_curve(in_request: int) -> tuple:
    sql_query = VIEWS[in_request].query

    df = execute_sql(VIEWS[in_request].query)
    data = df.to_dict('records')
    columns = [{'id': col, 'name': col} for col in df.columns]

    return sql_query, data, columns