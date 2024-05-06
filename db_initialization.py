from data.db_connector import excute_sql_file, execute_sql, copy_to_sql
from data.data_processing import select_rename_columns, DataFrame_to_buffer

from pandas import read_csv
import pandas as pd

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

    file_path, table = f'{PATH_TO_DATA}wedding/Dep2.csv', 'etat_matrimonial_anterieur_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    file_path, table = f'{PATH_TO_DATA}wedding/Dep4.csv', 'nationalite_epoux'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_DOMI'].str.contains('XX')) | (df['REGDEP_DOMI'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    file_path, table = f'{PATH_TO_DATA}wedding/Dep6.csv', 'repartition_mensuelle_mariage'
    df = read_csv(file_path, sep=';')
    df = df[~((df['REGDEP_MAR'].str.contains('XX')) | (df['REGDEP_MAR'].str.len() < 4))] # Filtration des données
    df = select_rename_columns(df, table)
    copy_to_sql(DataFrame_to_buffer(df), table)

    # Pour le dossier pop_census

    # file_path, table = f'{PATH_TO_DATA}pop_census/base-cc-serie-historique-2020.CSV', 'population'
    # df = read_csv(file_path, sep=';', dtype='object')
    # df = df[~df['CODGEO'].str.startswith('97')]

    # stat_mapping = {
    #     'P20_POP': ('Population', 2020),
    #     'P14_POP': ('Population', 2014),
    #     'P09_POP': ('Population', 2009),
    #     'D99_POP': ('Population', 1999),
    #     'D90_POP': ('Population', 1990),
    #     'D82_POP': ('Population', 1982),
    #     'D75_POP': ('Population', 1975),
    #     'NAIS1420': ('Naissances', 2014, 2020),
    #     'NAIS0914': ('Naissances', 2009, 2014),
    #     'NAIS9909': ('Naissances', 1999, 2009),
    #     'NAIS9099': ('Naissances', 1990, 1999),
    #     'NAIS8290': ('Naissances', 1982, 1990),
    #     'NAIS7582': ('Naissances', 1975, 1982),
    #     'NAIS6875': ('Naissances', 1968, 1975),
    #     'DECE1420': ('Décès', 2014, 2020),
    #     'DECE0914': ('Décès', 2009, 2014),
    #     'DECE9909': ('Décès', 1999, 2009),
    #     'DECE9099': ('Décès', 1990, 1999),
    #     'DECE8290': ('Décès', 1982, 1990),
    #     'DECE7582': ('Décès', 1975, 1982),
    #     'DECE6875': ('Décès', 1968, 1975),
    #     'P20_LOG': ('Nombre de Logements', 2020),
    #     'P14_LOG': ('Nombre de Logements', 2014),
    #     'P09_LOG': ('Nombre de Logements', 2009), 
    #     'D99_LOG': ('Nombre de Logements', 1999),
    #     'D90_LOG': ('Nombre de Logements', 1990),
    #     'D82_LOG': ('Nombre de Logements', 1982),
    #     'D75_LOG': ('Nombre de Logements', 1975),
    #     'D68_LOG': ('Nombre de Logements', 1968),
    #     'P20_RP': ('Nombre de résidences principales', 2020),
    #     'P14_RP': ('Nombre de résidences principales', 2014),
    #     'P09_RP': ('Nombre de résidences principales', 2009),
    # }

    # transformed_df = pd.DataFrame(columns=['codgeo', 'annee', 'annee2', 'type_statistique', 'valeur'])

    # for colonne in df.columns:
    #     if colonne in stat_mapping:
    #         type_statistique, *annees = stat_mapping[colonne]
    #         if len(annees) == 1:
    #             annee, annee2 = annees[0], None
    #         else:
    #             annee, annee2 = annees
    #         temp_df = pd.DataFrame({'codgeo': df['CODGEO'], 'annee': annee, 'annee2': annee2, 'type_statistique': type_statistique, 'valeur': df[colonne]})
    #         transformed_df = pd.concat([transformed_df, temp_df], ignore_index=True)

    # df = select_rename_columns(df, table)
    # copy_to_sql(DataFrame_to_buffer(transformed_df), table)

    # ALTER TABLES
    excute_sql_file(f'{PATH_TO_SQL}alter_tables.sql')

    # UPDATE TABLES
    excute_sql_file(f'{PATH_TO_SQL}update_tables.sql')
   
    # TEST SELECT
    # print(execute_sql('SELECT * FROM region;'))