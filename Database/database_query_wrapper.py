# script designed to wrap calling queries to db
import sqlite3
import pandas as pd

def run_query(query):
    data = []
    try:
        connection = sqlite3.connect("fpa-database.db")
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    except sqlite3.Error as error:
        print('Running query: "{query}" failed - {error}'.format(query = query, error = error))
    finally:
        if (connection):
            connection.close()
        return data

def run_query_pandas(query):
    data = pd.DataFrame()
    try:
        connection = sqlite3.connect("fpa-database.db")
        data = pd.read_sql_query(query, connection)
    except sqlite3.Error as error:
        print('Running query: "{query}" failed - {error}'.format(query = query, error = error))
    finally:
        if (connection):
            connection.close()
        return data
