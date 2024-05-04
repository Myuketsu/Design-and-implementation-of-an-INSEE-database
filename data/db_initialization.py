from db_connector import excute_sql_file, execute_sql
from data_processing import select_and_rename_csv

PATH_TO_SQL = './data/sql/'

if __name__ == '__main__':
    # CREATE TABLES
    excute_sql_file(f'{PATH_TO_SQL}create_tables.sql')

    # INSERT (COPY)
    # file_path, table = './data/raw_data/area/v_region_2023.csv', 'region'
    # copy_to_sql(select_and_rename_csv(file_path, table), table)
    
    # TEST SELECT
    # print(execute_sql('SELECT * FROM region;'))