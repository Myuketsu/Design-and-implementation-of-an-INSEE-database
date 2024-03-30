from configparser import ConfigParser
import psycopg2

CONFIG_PATH = './data/config.ini'

def get_cursor() -> psycopg2.extensions.cursor:
    config = ConfigParser()
    config.read(CONFIG_PATH)

    conn: psycopg2.extensions.connection
    with psycopg2.connect(**config['DATABASE']) as conn:
        return conn.cursor()