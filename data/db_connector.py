from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection

from pandas import DataFrame, read_csv

from io import StringIO

from data_processing import load_config, select_and_rename_csv

__POOL: SimpleConnectionPool = SimpleConnectionPool(
    minconn=2, maxconn=8,
    **load_config('database')
)

def execute_sql(query: str) -> DataFrame | None:
    conn: connection = __POOL.getconn()
    with conn.cursor() as cursor:
        cursor.execute(query)

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