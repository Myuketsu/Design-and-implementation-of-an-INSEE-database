from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection
from psycopg2.pool import PoolError

from pandas import DataFrame

from io import StringIO

from data.data_processing import load_config

__POOL: SimpleConnectionPool = SimpleConnectionPool(
    minconn=2, maxconn=8,
    **load_config('database')
)

def execute_sql(query: str, vars: tuple | list | dict=None) -> DataFrame | None:
    """
    Exécute UNE requête SQL avec des variables associées et renvoie les résultats sous forme de DataFrame pandas
    ou None si la requête ne renvoie aucune donnée.

    Args
    ----
        query (str): La requête SQL à exécuter.
        vars (tuple | list | dict): Les variables associées à la requête, sous forme de tuple, liste ou dictionnaire.

    Returns
    -------
        DataFrame | None: Un DataFrame pandas contenant les résultats de la requête si celle-ci renvoie des données, sinon None.

    Remarques
    ---------
        Cette fonction utilise une connexion issue d'un pool de connexions pour exécuter la requête SQL. Une fois la
        requête exécutée, la connexion est automatiquement libérée dans le pool. Si la requête ne renvoie aucune donnée
        (par exemple, une requête INSERT, UPDATE ou DELETE), la fonction renvoie None.

    See Also
    --------
        execute : Execute a database operation (query or command)(https://www.psycopg.org/docs/cursor.html#cursor.execute).

    Exemple
    -------
        >>> # Exemple d'utilisation avec une requête SELECT
        >>> execute_sql('SELECT * FROM table WHERE condition = %s;', (valeur,))
        ...
        >>> # Exemple d'utilisation avec une requête INSERT
        >>> execute_sql('INSERT INTO table (colonne1, colonne2) VALUES (%s, %s);', (valeur1, valeur2))
        ...
    """
    try:
        conn: connection = __POOL.getconn()
    except PoolError as e:
        print(e.pgerror)
        return None
    
    query_result = None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, tuple() if vars is None else vars)

            if cursor.description is None:
                conn.commit()
            else:
                query_result = DataFrame(
                    data=cursor.fetchall(),
                    columns=[column.name for column in cursor.description]
                )
    except Exception as e: # On ne gère pas l'erreur ici !
        print(f'Une erreur est survenue lors de la requête.\nSQL : {query.replace('\n', ' ')}')
        raise e
    finally: # On redonne la connexion dans tout les cas
        __POOL.putconn(conn)
    return query_result

def excute_sql_file(file_name: str) -> None:
    with open(file_name, 'r') as sql_file:
        execute_sql(sql_file.read())

def copy_to_sql(file: StringIO, table: str, sep: str=',') -> None:
    columns = file.readline().replace('\r\n', '').split(',')

    conn: connection = __POOL.getconn()
    with conn.cursor() as cursor:
        cursor.copy_from(
            file=file,
            table=table,
            columns=columns,
            sep=sep
        )
        conn.commit()

    __POOL.putconn(conn)