from dash import html, register_page, dcc
from dash import callback, Input, Output, State, ctx, no_update
import dash_mantine_components as dmc

import data.db_connector as db_connector

register_page(__name__, path='/transactions', name='Transactions', title='Transactions', order=9, icon='grommet-icons:transaction')

SELECT = 'SELECT * FROM statistiques_pop WHERE code_commune = \'33063\' AND type_statistique = \'transaction\' AND annee_debut = 1000'
TRANSACTION = '''BEGIN;\nINSERT INTO statistiques_pop (code_commune, type_statistique, annee_debut, annee_fin, valeur) VALUES (\'33063\', \'transaction\', 1000, 1000, 1.0) ON CONFLICT DO NOTHING;'''

def layout():
    return html.Div(
        [
            dcc.Store(id='id_connection'),
            dmc.Title(dmc.Text('Transactions', weight=700), order=4),
            dmc.Text('Exemple d\'utilisation : Appuyer sur \'EXECUTE SQL\'. Sur une autre page, vérifier si l\'insertion s\'est faite avec le bouton \'READ TRANSACTION\'. Retouner sur la première page, appuyer sur le bouton \'COMMIT TRANSACTION\'. Allez sur la deuxième page, constater que le commit s\'est bien effectué (avec le bouton \'READ TRANSACTION\').'),
            dmc.Text('Le bouton \'DELETE DATA FROM INSERTION\' supprime les données insérées.'),
            dmc.Prism(TRANSACTION, language='sql', withLineNumbers=True),
            html.Div(
                [
                    dmc.Button('EXECUTE SQL', id='transactions_execute', n_clicks=0),
                    dmc.Button('COMMIT TRANSACTION', id='transactions_commit', n_clicks=0, disabled=True)
                ], 
                style={'display': 'flex', 'columnGap': '10px'}
            ),
            dmc.Divider(style={'margin': '10px 0px'}),
            html.Div(
                [
                    dmc.Button('READ TRANSACTION', id='transactions_select', n_clicks=0),
                    dmc.Button('DELETE DATA FROM INSERTION', color='red', id='transactions_delete', n_clicks=0)
                ],
                style={'display': 'flex', 'columnGap': '10px'}
            ),
            dmc.Text('', id='transactions_result')
        ],
        style={'display': 'flex', 'flexDirection': 'column', 'padding': '15px', 'rowGap': '10px'}
    )

@callback(
    [
        Output('transactions_execute', 'disabled'),
        Output('transactions_commit', 'disabled'),
        Output('transactions_select', 'disabled'),
        Output('transactions_delete', 'disabled'),
        Output('transactions_result', 'children'),
        Output('id_connection', 'data')
    ],
    [
        Input('transactions_execute', 'n_clicks'),
        Input('transactions_commit', 'n_clicks'),
        Input('transactions_select', 'n_clicks'),
        Input('transactions_delete', 'n_clicks')
    ],
    [
        State('id_connection', 'data')
    ],
    prevent_initial_call=True)
def show_notification_update(in_execute: int, in_commit: int, in_select: int, in_delete: int, state_id: str) -> tuple:
    execute, commit, select, delete, result, user_key = [no_update] * 6
    if ctx.triggered_id == 'transactions_execute':
        key = db_connector.get_random_key()
        for query in TRANSACTION.split('\n'):
            db_connector.get_and_execute_transaction(query, key)
        execute, commit, select, delete, result, user_key = True, False, True, True, '', key
    elif ctx.triggered_id == 'transactions_delete':
        db_connector.execute_sql(f'''DELETE FROM statistiques_pop WHERE code_commune = \'33063\' AND type_statistique = \'transaction\' AND annee_debut = 1000 AND EXISTS ({SELECT});''')
        result = ''
    elif ctx.triggered_id == 'transactions_commit':
        db_connector.commit_and_put_conn_transaction(state_id)
        execute, commit, select, delete = False, True, False, False
    elif ctx.triggered_id == 'transactions_select':
        df = db_connector.execute_sql(SELECT)
        if len(df):
            result = 'Les données insérées sont bien dans la base de données.'
        else:
            result = 'Les données n\'ont pas encore été insérées...'

    return execute, commit, select, delete, result, user_key