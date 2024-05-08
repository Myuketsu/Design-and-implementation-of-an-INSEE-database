from dash import html, register_page
from dash import callback, Input, Output, State, ctx
import dash_mantine_components as dmc
from dash.dash_table import DataTable

from psycopg2.errors import RaiseException

from data.db_connector import execute_sql
from data.data_processing import SQL_PATH, get_file_content

from numpy.random import rand

register_page(__name__, path='/triggers', name='Triggers', title='Triggers', order=5, category_name='Triggers')

REQUEST = 'SELECT C.nom AS Com_nom, S.valeur AS Com_pop, D.nom AS Dep_nom, D.population AS Dep_pop, R.nom AS Reg_nom, R.population AS Reg_pop FROM commune C JOIN departement D ON C.code_departement = D.code JOIN region R ON D.code_region = R.code JOIN (SELECT * FROM statistiques_pop WHERE type_statistique = \'population\' AND annee_debut = \'2020\') S ON C.code = S.code_commune WHERE C.nom = \'Bordeaux\';'
ACTIONS = {
    'triggers_controls_insert': ('INSERT', 'INSERT INTO %s VALUES (999);'),
    'triggers_controls_update': ('UPDATE', 'UPDATE %s SET population = -999 WHERE code = \'75\';'),
    'triggers_controls_delete': ('DELETE', 'DELETE FROM %s WHERE code = \'75\';'),
}

def layout():
    return html.Div(
        [
            html.Div(id='triggers_notifications_container'),
            control_and_result_side(),
            code_box()
        ],
        id='triggers_layout'
    )

def control_and_result_side():
    return html.Div(
        [
            controls(),
            dmc.Divider(),
            result_table()
        ],
        id='triggers_control_and_result_side'
    )

def controls():
    return html.Div(
        [
            dmc.Title('Déclencheur du trigger : Bloqueur', order=4, transform='uppercase'),
            dmc.RadioGroup(
                [dmc.Radio(label, value=value) for label, value in [['Département', 'departement'], ['Région', 'region']]],
                id='triggers_controls_radiogroup',
                value='departement',
                label=dmc.Title('Sélection de la table', order=6),
                size='sm',
            ),
            html.Div(
                [
                    dmc.Button('INSERT', id='triggers_controls_insert', n_clicks=0),
                    dmc.Button('UPDATE', id='triggers_controls_update', n_clicks=0),
                    dmc.Button('DELETE', id='triggers_controls_delete', n_clicks=0)
                ],
                id='triggers_buttons_groups'
            )
        ],
        id='triggers_controls'
    )

def result_table():
    df = execute_sql(REQUEST)
    return html.Div(
        [
            dmc.Title('Déclencheur du trigger : Population', order=4, transform='uppercase', style={'margin': 'auto'}),
            dmc.NumberInput(
                label='Quantité d\'habitant à ajouter à Bordeaux',
                value=100,
                min=0,
                step=50,
                style={'width': 300, 'margin': 'auto'},
                id='triggers_add_number'
            ),
            DataTable(
                data=df.to_dict('records'),
                columns=[{'id': col, 'name': col} for col in df.columns],
                page_size=2,
                style_table={
                    'border-left': '1px solid rgb(233, 236, 239)',
                    'border-right': '1px solid rgb(233, 236, 239)'
                },
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                id='triggers_table'
            )
        ],
        id='triggers_result_table'
    )

def code_box():
    return html.Div(
        [
            html.Div(
                [
                    dmc.Prism(
                        get_file_content(f'{SQL_PATH}triggers.sql'),
                        language='sql',
                        withLineNumbers=True,
                        id='triggers_code_highlight'
                    )
                ],
                id='triggers_code_box',
                className='layout_code_highlight'
            )
        ],
        id='triggers_code_box_box'
    )

# --- CALLBACKS ---

@callback(
    [
        Output('triggers_notifications_container', 'children')
    ],
    [
        Input('triggers_controls_insert', 'n_clicks'),
        Input('triggers_controls_update', 'n_clicks'),
        Input('triggers_controls_delete', 'n_clicks')
    ],
    [
        State('triggers_controls_radiogroup', 'value')
    ],
    prevent_initial_call=True)
def show_notification_blocker(in_insert: int, in_update: int, in_delete: int, state_radiogroup: str) -> tuple:
    message = ''
    try:
        execute_sql(ACTIONS[ctx.triggered_id][1] % state_radiogroup)
    except RaiseException as e:
        message = e.pgerror.split('\n')

    return dmc.Notification(
        title=f'L\'action {ACTIONS[ctx.triggered_id][0]} a été bloqué',
        action='show',
        message=message,
        color='red',
        id=f'triggers_simple_notification-{rand()}'
    ),

@callback(
    [
        Output('triggers_table', 'data')
    ],
    [
        Input('triggers_add_number', 'value')
    ],
    prevent_initial_call=True)
def show_notification_update(in_number: int) -> tuple:
    execute_sql('UPDATE statistiques_pop SET valeur = valeur + %s WHERE type_statistique = \'population\' AND annee_debut = \'2020\' AND code_commune = \'33063\';', [in_number])
    return execute_sql(REQUEST).to_dict('records'),