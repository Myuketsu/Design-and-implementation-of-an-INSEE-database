from data.db_connector import excute_sql_file, copy_to_sql, execute_sql
from data.data_processing import select_rename_columns, DataFrame_to_buffer, population_preprocessing, load_query

from pandas import read_csv
from time import perf_counter

PATH_TO_SQL = './data/sql/'
PATH_TO_DATA = './data/raw_data/'

def timeit(func, *args, **kwargs):
    start_time = perf_counter()
    result = func(*args, **kwargs)
    total_time = perf_counter() - start_time

    print(f'Temps d\'exécution {total_time:.5f}s')
    return result

if __name__ == '__main__':
    # CREATE TABLES
    print('Création des tables', end=' - ')
    timeit(excute_sql_file, f'{PATH_TO_SQL}create_tables.sql')

    # # INSERT (COPY)

    # # Pour le dossier area

    print('\nDossier area\nCopy region', end=' - ')
    file_path, table = f'{PATH_TO_DATA}area/v_region_2023.csv', 'region'
    df = read_csv(file_path)
    df = df[df['CHEFLIEU'].map(lambda x: int(x) < 97000 if x.isnumeric() else True)]
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy departement', end=' - ')
    file_path, table = f'{PATH_TO_DATA}area/v_departement_2023.csv', 'departement'
    df = read_csv(file_path)
    df = df[df['DEP'].map(len) < 3]
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy commune', end=' - ')
    file_path, table = f'{PATH_TO_DATA}area/v_commune_2023.csv', 'commune'
    df = read_csv(file_path) # Lecture du fichier CSV
    df = df[df['TYPECOM'].isin(['COM', 'ARM'])] # Filtration des données
    df = df[df['COM'].map(lambda x: int(x) < 97000 if x.isnumeric() else True)]
    df = select_rename_columns(df, table) # Sélection et renommage des colonnes d'intérêts
    timeit(copy_to_sql, DataFrame_to_buffer(df), table) # Envoie par COPY des données à la BD

    print('Copy cheflieuregion', end=' - ')
    file_path, table = f'{PATH_TO_DATA}area/v_region_2023.csv', 'cheflieuregion'
    df = read_csv(file_path)
    df = df[df['CHEFLIEU'].map(lambda x: int(x) < 97000 if x.isnumeric() else True)]
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy cheflieudepartement', end=' - ')
    file_path, table = f'{PATH_TO_DATA}area/v_departement_2023.csv', 'cheflieudepartement'
    df = read_csv(file_path)
    df = df[df['DEP'].map(len) < 3]
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    # # Pour le dossier wedding

    print('\nDossier wedding\nCopy mariage', end=' - ')
    file_path, table = f'{PATH_TO_DATA}wedding/Dep1.csv', 'mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy premier_mariage', end=' - ')
    file_path, table = f'{PATH_TO_DATA}wedding/Dep3.csv', 'premier_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy pays_mariage', end=' - ')
    file_path, table = f'{PATH_TO_DATA}wedding/Dep5.csv', 'pays_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_DOMI'].str.contains('XX')) | (df['REGDEP_DOMI'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy etat_matrimonial_anterieur_mariage', end=' - ')
    file_path, table = f'{PATH_TO_DATA}wedding/Dep2.csv', 'etat_matrimonial_anterieur_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy nationalite_epoux', end=' - ')
    file_path, table = f'{PATH_TO_DATA}wedding/Dep4.csv', 'nationalite_epoux'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_DOMI'].str.contains('XX')) | (df['REGDEP_DOMI'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    print('Copy repartition_mensuelle_mariage', end=' - ')
    file_path, table = f'{PATH_TO_DATA}wedding/Dep6.csv', 'repartition_mensuelle_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    # Pour le dossier pop_census

    print('\nDossier pop_census\nCopy statistiques_pop', end=' - ')
    file_path, table = f'{PATH_TO_DATA}pop_census/base-cc-serie-historique-2020.CSV', 'statistiques_pop'
    df = read_csv(file_path, sep=';', dtype='object')
    df = population_preprocessing(df, table)
    timeit(copy_to_sql, DataFrame_to_buffer(df), table)

    # ALTER TABLES
    print('\nAltération des tables', end=' - ')
    timeit(excute_sql_file, f'{PATH_TO_SQL}alter_tables.sql')

    # UPDATE TABLES
    print('\nMise à jour des tables', end=' - ')
    timeit(excute_sql_file, f'{PATH_TO_SQL}update_tables.sql')

    # Création des vues
    print('\nCréation des vues')
    query_file = load_query(f'{PATH_TO_SQL}create_views.toml')
    for view, item in query_file.items():
        print(f'Vue : {view}', end=' - ')
        timeit(execute_sql, item.get('view_sql'))

    # PROCEDURE
    print('\nProcedure stockée', end=' - ')
    timeit(excute_sql_file, f'{PATH_TO_SQL}procedure.sql')

    # TRIGGERS
    print('\nTriggers', end=' - ')
    timeit(excute_sql_file, f'{PATH_TO_SQL}triggers.sql')