from data.db_connector import excute_sql_file

PATH_TO_SQL = './data/sql/'

if __name__ == '__main__':
    # ALTER TABLES
    excute_sql_file(f'{PATH_TO_SQL}alter_tables.sql')