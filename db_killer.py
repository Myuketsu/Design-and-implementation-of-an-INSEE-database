from data.db_connector import excute_sql_file

PATH_TO_SQL = './data/sql/'

if __name__ == '__main__':
    # DROP TABLES
    excute_sql_file(f'{PATH_TO_SQL}drop_tables.sql')