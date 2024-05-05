from data.db_connector import excute_sql_file, execute_sql, copy_to_sql
from data.data_processing import select_rename_columns, DataFrame_to_buffer

from pandas import read_csv

PATH_TO_SQL = './data/sql/'

if __name__ == '__main__':
    # DROP TABLES
    excute_sql_file(f'{PATH_TO_SQL}drop_tables.sql')