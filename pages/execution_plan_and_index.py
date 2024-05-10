from dash import html, register_page
from dash import callback, Input, Output
from dash.dash_table import DataTable
import dash_mantine_components as dmc
from dash.dcc import Markdown

from collections import namedtuple

from data.db_connector import execute_sql
from data.data_processing import load_query

import pandas as pd

register_page(__name__, path='/execution_plan_and_index', name='Index', title='Plan d\'exécution et Index', order=8, category_name='Plan d\'exécution')

query_file = load_query('./data/sql/explain_index.toml')

Explain = namedtuple('ExplainIndex', ['title', 'desc', 'queries', 'explain'])
EXPLAIN: list[Explain] = [
    Explain(item.get('title'), item.get('desc'), item.get('queries'), item.get('explain'))
    for item in query_file.values()
]

# --- LAYOUT ---

def layout():
    return html.Div(
        [
            explain_selector_index(),
            explain_body_index(),
            explain_description_index()
        ],
        id='EXPLAIN_layout_index'
    )

def explain_selector_index() -> html.Div:
    data = [
        {'value': index, 'label': explain.title} for index, explain in enumerate(EXPLAIN)
    ]
    return html.Div(
        [
            html.Div(
                [
                    dmc.Select(
                        label=dmc.Text('Selection de la requête à EXPLAIN', weight=700),
                        value=0,
                        data=data,
                        id='explain_selector_index'
                    )
                ],
                id='explain_selector_index_box'
            ),
            html.Div(className='separator'),
            html.Div(
                [
                    dmc.Title('Contenu de la requête SQL', order=6),
                    dmc.Prism(
                        '\n'.join(EXPLAIN[0].queries),
                        language='sql',
                        withLineNumbers=True,
                        id='explain_selector_index_SQL_viewer'
                    )
                ],
                id='explain_selector_index_SQL'
            )
        ],
        id='explain_selector_index_body'
    )

def explain_body_index() -> html.Div:
    delete_index()
    results = []
    for query in EXPLAIN[0].queries:
        df = execute_sql(query)
        results.append(df)
    final_df = pd.concat(results)

    return html.Div(
        [
            dmc.Title(EXPLAIN[0].desc, order=6, id='explain_body_index_table_title'),
            DataTable(
                data=final_df.to_dict('records'),
                columns=[{'id': col, 'name': col} for col in final_df.columns],
                page_size=15,
                style_table={
                    'border-left': '1px solid rgb(233, 236, 239)',
                    'border-right': '1px solid rgb(233, 236, 239)'
                },
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                id='explain_body_index_table'
            )
        ],
        id='explain_body_index'
    )


def explain_description_index() -> html.Div:

    return html.Div(
        [
            Markdown(EXPLAIN[0].explain, id='explain_result_index'),

        ],
        id='explain_description_index'
    )

def delete_index():
    execute_sql("DROP INDEX IF EXISTS idx_population_value;")
    execute_sql("DROP INDEX IF EXISTS idx_iddep;")
    execute_sql("DROP INDEX IF EXISTS idx_code_departement;")
    execute_sql("DROP INDEX IF EXISTS idx_type_statistique;")
    execute_sql("DROP INDEX IF EXISTS idx_annee_debut;")


# --- CALLBACKS ---

@callback(
    [
        Output('explain_selector_index_SQL_viewer', 'children'),
        Output('explain_body_index_table', 'data'),
        Output('explain_body_index_table', 'columns'),
        Output('explain_body_index_table', 'page_current'),
        Output('explain_body_index_table_title', 'children'),
        Output('explain_result_index', 'children')
    ],
    [
        Input('explain_selector_index', 'value')
    ])

def update_reconstructed_curve(in_explain: int) -> tuple:
    delete_index()
    sql_query = '\n'.join(EXPLAIN[in_explain].queries)

    results = []
    for query in EXPLAIN[in_explain].queries:
        df = execute_sql(query)
        results.append(df)
    final_df = pd.concat(results)
    data = final_df.to_dict('records')
    columns = [{'id': col, 'name': col} for col in final_df.columns]

    desc_table = EXPLAIN[in_explain].desc
    explain = EXPLAIN[in_explain].explain

    return sql_query, data, columns, 0, desc_table, explain