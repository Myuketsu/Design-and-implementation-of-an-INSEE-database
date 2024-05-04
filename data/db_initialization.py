from db_connector import excute_sql_file

PATH_TO_SQL = './data/sql/'

if __name__ == '__main__':
    excute_sql_file(f'{PATH_TO_SQL}create_tables.sql')
    # excute_sql_file('insert_data.sql')