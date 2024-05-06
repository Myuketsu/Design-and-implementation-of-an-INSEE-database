from data.db_connector import excute_sql_file, execute_sql, copy_to_sql
from data.data_processing import select_rename_columns, DataFrame_to_buffer, population_preprocessing

from pandas import read_csv

PATH_TO_SQL = './data/sql/'
PATH_TO_DATA = './data/raw_data/'

if __name__ == '__main__':
    # CREATE TABLES
    excute_sql_file(f'{PATH_TO_SQL}create_tables.sql')

    # # INSERT (COPY)

    # # Pour le dossier area

    file_path, table = f'{PATH_TO_DATA}area/v_region_2023.csv', 'region'
    df = read_csv(file_path)
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    file_path, table = f'{PATH_TO_DATA}area/v_departement_2023.csv', 'departement'
    df = read_csv(file_path)
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    file_path, table = f'{PATH_TO_DATA}area/v_commune_2023.csv', 'commune'
    df = read_csv(file_path) # Lecture du fichier CSV
    df = df[df['TYPECOM'] == 'COM'] # Filtration des données
    df = select_rename_columns(df, table) # Sélection et renommage des colonnes d'intérêts
    copy_to_sql(DataFrame_to_buffer(df), table) # Envoie par COPY des données à la BD

    file_path, table = f'{PATH_TO_DATA}area/v_region_2023.csv', 'cheflieuregion'
    df = read_csv(file_path)
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    file_path, table = f'{PATH_TO_DATA}area/v_departement_2023.csv', 'cheflieudepartement'
    df = read_csv(file_path)
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    # # Pour le dossier wedding

    file_path, table = f'{PATH_TO_DATA}wedding/Dep1.csv', 'mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    file_path, table = f'{PATH_TO_DATA}wedding/Dep3.csv', 'premier_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    file_path, table = f'{PATH_TO_DATA}wedding/Dep5.csv', 'pays_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_DOMI'].str.contains('XX')) | (df['REGDEP_DOMI'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    # Pour le dossier pop_census

    file_path, table = f'{PATH_TO_DATA}pop_census/base-cc-serie-historique-2020.CSV', 'population'
    df = read_csv(file_path, sep=';', dtype='object')
    df = population_preprocessing(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    # ALTER TABLES
    excute_sql_file(f'{PATH_TO_SQL}alter_tables.sql')

    # UPDATE TABLES
    excute_sql_file(f'{PATH_TO_SQL}update_tables.sql')
   
    # TEST SELECT
    # print(execute_sql('SELECT * FROM region;'))