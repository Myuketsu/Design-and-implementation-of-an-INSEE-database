from dash import html, register_page
from dash import callback, Input, Output, State, ctx
import dash_mantine_components as dmc

from dash.dash_table import DataTable
from data.db_connector import execute_sql
from data.data_processing import SQL_PATH, get_file_content

register_page(__name__, path='/triggers_suite', name='Suite', title='Triggers suite', order=6, category_name='Triggers')

REQUEST_DEP = '''SELECT D.code AS code_dep, D.nom AS nom_dep, DP.annee, DP.population FROM departement_pop DP JOIN departement D ON D.code = DP.code_departement WHERE annee = '2024';'''
REQUEST_REG = '''SELECT R.code AS code_reg, R.nom AS nom_reg, RP.annee, RP.population FROM region_pop RP JOIN region R ON R.code = RP.code_region WHERE annee = '2024';'''

def layout():
    return html.Div(
        [
            result_table(),
            code_box()
        ],
        id='triggers_suite_layout'
    )

def result_table():
    df_dep = execute_sql(REQUEST_DEP)
    df_reg = execute_sql(REQUEST_REG)
    return html.Div(
        [
            dmc.Title('Insertion de données dans un département', order=4, transform='uppercase', style={'margin': '0 auto'}),
            dmc.Text('L\'insertion se fera en 2024 et la population sera égale à 1 pour chaque commune.\n(La Corse se compose de deux régions : \'Haute-Corse\', \'Corse-du-Sud\')', style={'margin': '0 auto'}),
            html.Div(
                [
                    dmc.Select(
                        id='triggers_suite_select',
                        value='33',
                        searchable=True,
                        data=execute_sql('SELECT code, nom FROM departement;').rename(columns={'code': 'value', 'nom': 'label'}).to_dict('records'),
                        style={'width': 200},
                    ),
                    dmc.Button('INSÉRER', id='triggers_suite_button_insert', n_clicks=0),
                    dmc.Button('RESET POP', id='triggers_suite_button_reset', n_clicks=0, color='red')
                ],
                id='triggers_suite_buttons_groups'
            ),
            DataTable(
                data=df_dep.to_dict('records'),
                columns=[{'id': col, 'name': col} for col in df_dep.columns],
                page_size=10,
                style_table={
                    'border-left': '1px solid rgb(233, 236, 239)',
                    'border-right': '1px solid rgb(233, 236, 239)'
                },
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                id='triggers_suite_table_departement'
            ),
            DataTable(
                data=df_reg.to_dict('records'),
                columns=[{'id': col, 'name': col} for col in df_reg.columns],
                page_size=10,
                style_table={
                    'border-left': '1px solid rgb(233, 236, 239)',
                    'border-right': '1px solid rgb(233, 236, 239)'
                },
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                id='triggers_suite_table_region'
            )
        ],
        id='triggers_suite_result_table'
    )

def code_box():
    return html.Div(
        [
            html.Div(
                [
                    dmc.Prism(
                        get_file_content(f'{SQL_PATH}triggers_suite.sql'),
                        language='sql',
                        withLineNumbers=True,
                        id='triggers_suite_code_highlight'
                    )
                ],
                id='triggers_suite_code_box',
                className='layout_code_highlight'
            )
        ],
        id='triggers_suite_code_box_box'
    )

@callback(
    [
        Output('triggers_suite_table_departement', 'data'),
        Output('triggers_suite_table_region', 'data'),
    ],
    [
        Input('triggers_suite_button_insert', 'n_clicks'),
        Input('triggers_suite_button_reset', 'n_clicks')
    ],
    [
        State('triggers_suite_select', 'value')
    ],
    prevent_initial_call=True)
def table_update_triggers_insert(in_btn_insert: int, in_btn_reset: int, state_select: int) -> tuple:
    if ctx.triggered_id == 'triggers_suite_button_insert':
        df_com_from_dep = execute_sql('SELECT code FROM commune WHERE code_departement = %s;', [state_select])
        str_builder = 'INSERT INTO statistiques_pop (code_commune, type_statistique, annee_debut, annee_fin, valeur) VALUES\n'
        str_builder += ('(\'' + df_com_from_dep['code'] + '\', \'population\', \'2024\', \'2024\', 1)').str.cat(sep=',\n')
        str_builder += '\nON CONFLICT DO NOTHING;'

        execute_sql(str_builder)

    elif ctx.triggered_id == 'triggers_suite_button_reset':
        execute_sql('DELETE FROM statistiques_pop WHERE type_statistique = \'population\' AND annee_debut = \'2024\';')
        execute_sql('DELETE FROM departement_pop WHERE annee = \'2024\';')
        execute_sql('DELETE FROM region_pop WHERE annee = \'2024\';')

    df_dep = execute_sql(REQUEST_DEP)
    df_reg = execute_sql(REQUEST_REG)
    
    return df_dep.to_dict('records'), df_reg.to_dict('records')