import sqlite3

import Database.database_setup_utils as dsu
import pandas as pd

connection = dsu.create_connection()

sqlite_create_table_values = ''' CREATE TABLE IF NOT EXISTS player_values_transfermarkt (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            transfermarkt_player_id text NOT NULL,
                                            date_stamp timestamp  integer NOT NULL,
                                            player_value integer NOT NULL,
                                            player_club text NOT NULL,
                                            player_url text NOT NULL,
                                            FOREIGN KEY (transfermarkt_player_id) REFERENCES players_transfermarkt_singles (id) ON DELETE CASCADE
                                        ); '''


def insert_into_player_values_transfermarkt():
    cnx = sqlite3.connect('fpa-database-fix.db')

    df_transfermarkt = pd.read_sql_query("select * from player_values", cnx)

    print(df_transfermarkt)

    for index, row in df_transfermarkt.iterrows():

        try:
            cursor = cnx.cursor()

            sql_insert_into_clubs = '''INSERT INTO player_values_transfermarkt
                                          (transfermarkt_player_id,date_stamp,player_value,player_club, player_url)
                                           VALUES
                                          (?, ?, ?,?, ?)'''
            player_id = select_player_id_global_from_players_transfermarkt_id(row['transfermarkt_player_id'])
            data_tuple = (player_id, row['date_stamp'], row['player_value'], row['player_club'], row['player_url'])
            cursor.execute(sql_insert_into_clubs, data_tuple)
            cnx.commit()
        except sqlite3.Error as error:

            print("Error while creating a sqlite table", error)
        except Exception as e:
            print(e)
    if (cnx): cnx.close()


def select_player_id_global_from_players_transfermarkt_id(id):
    sqlite_connection = sqlite3.connect("fpa-database-fix.db")
    cursor = sqlite_connection.cursor()
    sql_select = '''select id from players_transfermarkt_singles where player_name = (select player_name from players_transfermarkt pt where id = ? group by player_name);'''
    data_tuple = (id,)
    cursor.execute(sql_select, data_tuple)

    rows = cursor.fetchall()
    sqlite_connection.close()

    for row in rows:
        return row[0]


cursor = connection.cursor()
cursor.execute(sqlite_create_table_values)
connection.commit()

insert_into_player_values_transfermarkt()
connection.commit()

connection.close()
