from dash import html, register_page
from dash import callback, Input, Output
from dash.dash_table import DataTable
import dash_mantine_components as dmc
from dash.dcc import Markdown

from collections import namedtuple

from data.db_connector import execute_sql
from data.data_processing import load_query

register_page(__name__, path='/execution_plan', name='Plan d\'exécution', title='Plan d\'exécution', order=7, category_name='Plan d\'exécution')

query_file = load_query('./data/sql/explain.toml')

Explain = namedtuple('Explain', ['title', 'desc', 'query', 'explain'])
EXPLAIN: list[Explain] = [
    Explain(item.get('title'), item.get('desc'), item.get('query'), item.get('explain'))
    for item in query_file.values()
]

# --- LAYOUT ---

def layout():
    return html.Div(
        [
            explain_selector(),
            explain_body(),
            explain_description()
        ],
        id='EXPLAIN_layout'
    )

def explain_selector() -> html.Div:
    data = [
        {'value': index, 'label': explain.title} for index, explain in enumerate(EXPLAIN)
    ]
    return html.Div(
        [
            html.Div(
                [
                    dmc.Select(
                        label=dmc.Text('Selection de la requête', weight=700),
                        value=0,
                        data=data,
                        id='explain_selector'
                    )
                ],
                id='explain_selector_box'
            ),
            html.Div(className='separator'),
            html.Div(
                [
                    dmc.Title('Contenu de la requête SQL', order=6),
                    dmc.Prism(
                        EXPLAIN[0].query,
                        language='sql',
                        withLineNumbers=True,
                        id='explain_selector_SQL_viewer'
                    )
                ],
                id='explain_selector_SQL'
            )
        ],
        id='explain_selector_body'
    )

def explain_body() -> html.Div:
    df = execute_sql(EXPLAIN[0].query)
    return html.Div(
        [
            dmc.Title(EXPLAIN[0].desc, order=6, id='explain_body_table_title'),
            DataTable(
                data=df.to_dict('records'),
                columns=[{'id': col, 'name': col} for col in df.columns],
                page_size=15,
                style_table={
                    'border-left': '1px solid rgb(233, 236, 239)',
                    'border-right': '1px solid rgb(233, 236, 239)'
                },
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                id='explain_body_table'
            )
        ],
        id='explain_body'
    )


def explain_description() -> html.Div:

    return html.Div(
        [
            Markdown(EXPLAIN[0].explain, id='explain_result'),

        ],
        id='explain_description'
    )


# --- CALLBACKS ---

@callback(
    [
        Output('explain_selector_SQL_viewer', 'children'),
        Output('explain_body_table', 'data'),
        Output('explain_body_table', 'columns'),
        Output('explain_body_table', 'page_current'),
        Output('explain_body_table_title', 'children'),
        Output('explain_result', 'children')
    ],
    [
        Input('explain_selector', 'value')
    ])
def update_reconstructed_curve(in_explain: int) -> tuple:
    sql_query = EXPLAIN[in_explain].query

    df = execute_sql(EXPLAIN[in_explain].query)
    data = df.to_dict('records')
    columns = [{'id': col, 'name': col} for col in df.columns]

    desc_table = EXPLAIN[in_explain].desc
    explain = EXPLAIN[in_explain].explain

    return sql_query, data, columns, 0, desc_table, explain