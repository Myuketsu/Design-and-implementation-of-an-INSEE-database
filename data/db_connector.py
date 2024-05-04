from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection

from pandas import DataFrame, read_csv

from io import StringIO

from data_processing import load_config, select_and_rename_csv

__POOL: SimpleConnectionPool = SimpleConnectionPool(
    minconn=2, maxconn=8,
    **load_config('database')
)

def execute_sql(query: str, vars: tuple | list | dict) -> DataFrame | None:
    """
    Exécute une requête SQL avec des variables associées et renvoie les résultats sous forme de DataFrame pandas
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
        execute : Execute a database operation (query or command) (https://www.psycopg.org/docs/cursor.html#cursor.execute).

    Exemple
    -------
        >>> # Exemple d'utilisation avec une requête SELECT
        >>> execute_sql('SELECT * FROM table WHERE condition = %s;', (valeur,))
        ...
        >>> # Exemple d'utilisation avec une requête INSERT
        >>> execute_sql('INSERT INTO table (colonne1, colonne2) VALUES (%s, %s);', (valeur1, valeur2))
        ...
    """
    conn: connection = __POOL.getconn()
    with conn.cursor() as cursor:
        cursor.execute(query, vars)

        if cursor.description is None:
            conn.commit()
            query_result = None
        else:
            query_result = DataFrame(
                data=cursor.fetchall(),
                columns=[column.name for column in cursor.description]
            )

    __POOL.putconn(conn)
    return query_result

def excute_sql_file(file_name: str) -> None:
    with open(file_name, 'r') as sql_file:
        execute_sql(sql_file.read())

def copy_to_sql(file: StringIO, table: str, sep=',') -> None:
    conn: connection = __POOL.getconn()
    with conn.cursor() as cursor:
        cursor.copy_from(
            file=file,
            table=table,
            sep=sep
        )
        conn.commit()

    __POOL.putconn(conn)

if __name__ == '__main__':
    # file_path, table = './data/raw_data/area/v_region_2023.csv', 'region'
    # copy_to_sql(select_and_rename_csv(file_path, table), table)
        
    print(execute_sql('SELECT * FROM region;'))