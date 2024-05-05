from data.db_connector import excute_sql_file, execute_sql, copy_to_sql
from data.data_processing import select_rename_columns, DataFrame_to_buffer

from pandas import read_csv

PATH_TO_SQL = './data/sql/'
PATH_TO_DATA = './data/raw_data/'

if __name__ == '__main__':
    # CREATE TABLES
    # excute_sql_file(f'{PATH_TO_SQL}create_tables.sql')

    # INSERT (COPY)
    file_path, table = f'{PATH_TO_DATA}area/v_commune_2023.csv', 'region'
    df = read_csv(file_path) # Lecture du fichier CSV
    df = df[df['TYPECOM'] == 'COM'] # Filtration des données
    df = select_rename_columns(df) # Sélection et renommage des colonnes d'intérêts
    copy_to_sql(DataFrame_to_buffer(df), table) # Envoie par COPY des données à la BD
    
    # TEST SELECT
    # print(execute_sql('SELECT * FROM region;'))