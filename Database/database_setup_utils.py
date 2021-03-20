import sqlite3 as sql
import os

database_name = 'fpa-database.db'


def create_connection(db_name = database_name):
    connection = None
    try:
        connection = sql.connect(db_name)
        print(sql.version)
    except sql.Error as e:
        print(e)
        raise Exception('Creating database failure')
    return connection


def create_empty_database(db_name = database_name):
    if os.path.exists(db_name):
        os.remove(db_name)
    return create_connection(db_name)
