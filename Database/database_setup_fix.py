import sqlite3

from unidecode import unidecode
import Database.database_setup_utils as dsu
import pandas as pd

connection = dsu.create_connection()

sqlite_create_table_players_transfermarkt_singles = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt_singles (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            player_name text NOT NULL
                                        ); '''

sqlite_delete_table_players_transfermarkt_fpl = ''' DROP TABLE players_transfermarkt_fpl '''

sqlite_create_table_players_transfermarkt_fpl = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt_fpl (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            player_id_transfermarkt integer NOT NULL,
                                            player_id_fpl integer NOT NULL,
                                            player_name_transfermarkt text not null,
                                            first_name text not null,
                                            second_name text non null,
                                            FOREIGN KEY (player_id_transfermarkt) REFERENCES players_transfermarkt (id) ON DELETE CASCADE
                                        ); '''


def insert_into_players_transfermarkt_singles():
    cnx = sqlite3.connect('fpa-database-fix.db')

    df_transfermarkt = pd.read_sql_query("select player_name from players_transfermarkt group by player_name", cnx)

    print(df_transfermarkt)

    for index_transfer, row_transfer in df_transfermarkt.iterrows():

        try:
            cursor = cnx.cursor()
            sql_insert_into_clubs = '''INSERT INTO players_transfermarkt_singles (player_name)
                                                           VALUES
                                                          (?)'''

            data_tuple = (row_transfer['player_name'],)
            cursor.execute(sql_insert_into_clubs, data_tuple)
            cnx.commit()
        except sqlite3.Error as error:

            print("Error while creating a sqlite table", error)
        except Exception as e:
            print(e)
    if (cnx): cnx.close()


def insert_into_players_transfermarkt_fpl():
    cnx = sqlite3.connect('fpa-database-fix.db')

    df_transfer = pd.read_sql_query("SELECT * FROM players_transfermarkt_singles", cnx)
    print(df_transfer)

    df_fpl = pd.read_sql_query("SELECT * FROM players", cnx)

    for index_transfer, row_transfer in df_transfer.iterrows():
        for index_fpl, row_fpl in df_fpl.iterrows():
            if unidecode(row_transfer["player_name"]) == unidecode(
                    row_fpl["first_name"] + " " + row_fpl["second_name"]):
                try:
                    cursor = cnx.cursor()
                    sql_insert_into_clubs = '''INSERT INTO players_transfermarkt_fpl
                                                          (player_id_transfermarkt,player_id_fpl, player_name_transfermarkt, first_name, second_name)
                                                           VALUES
                                                          (?, ?, ?, ?, ?)'''

                    data_tuple = (
                        row_transfer['id'], row_fpl['guid'], row_transfer['player_name'], row_fpl['first_name'],
                        row_fpl['second_name'])
                    cursor.execute(sql_insert_into_clubs, data_tuple)
                    cnx.commit()
                except sqlite3.Error as error:

                    print("Error while creating a sqlite table", error)
                except Exception as e:
                    print(e)
    if (cnx): cnx.close()


def insert_into_players_transfermarkt_fpl_extra_time():
    cnx = sqlite3.connect('fpa-database-fix.db')

    df_transfer = pd.read_sql_query(
        "select * from players_transfermarkt_singles pt where pt.id not in (select player_id_transfermarkt from players_transfermarkt_fpl)",
        cnx)
    print(df_transfer)

    df_fpl = pd.read_sql_query(
        "select guid, first_name, second_name from players pt where guid not in (select player_id_fpl from players_transfermarkt_fpl);",
        cnx)

    for index_transfer, row_transfer in df_transfer.iterrows():
        for index_fpl, row_fpl in df_fpl.iterrows():
            if unidecode(row_fpl["second_name"]) in unidecode(row_transfer["player_name"]):
                counter = 0
                # zabezpieczenie na wypadek nazwisk typu James
                for index_transfer_2, row_transfer_2 in df_transfer.iterrows():
                    if unidecode(row_fpl["second_name"]) in unidecode(row_transfer_2["player_name"]):
                        counter = counter + 1
                if counter == 1:
                    try:
                        cursor = cnx.cursor()
                        sql_insert_into_clubs = '''INSERT INTO players_transfermarkt_fpl
                                                              (player_id_transfermarkt,player_id_fpl, player_name_transfermarkt, first_name, second_name)
                                                               VALUES
                                                              (?, ?, ?, ?, ?)'''

                        data_tuple = (
                            row_transfer['id'], row_fpl['guid'], row_transfer['player_name'], row_fpl['first_name'],
                            row_fpl['second_name'])
                        cursor.execute(sql_insert_into_clubs, data_tuple)
                        cnx.commit()
                    except sqlite3.Error as error:

                        print("Error while creating a sqlite table", error)
                    except Exception as e:
                        print(e)
    if (cnx): cnx.close()


def insert_into_players_transfermarkt_fpl_singles(name_transfer, first_name, second_name):
    cnx = sqlite3.connect('fpa-database-fix.db')

    cur = cnx.cursor()
    cur.execute("""select * 
             from players_transfermarkt_singles pt 
             where pt.player_name=?""", (name_transfer,))

    rows_transfer = cur.fetchall()

    cur.execute("""select guid, first_name, second_name from players pt where guid not in (select player_id_fpl from players_transfermarkt_fpl) 
         and second_name = ? and first_name =  ? """, (second_name, first_name))

    rows_fpl = cur.fetchall()

    print(rows_fpl[0])

    if len(rows_fpl) == 1 and len(rows_transfer) == 1:
        try:
            cursor = cnx.cursor()
            sql_insert_into_clubs = '''INSERT INTO players_transfermarkt_fpl
                                                                      (player_id_transfermarkt,player_id_fpl, player_name_transfermarkt, first_name, second_name)
                                                                       VALUES
                                                                      (?, ?, ?, ?, ?)'''

            data_tuple = (
                rows_transfer[0][0], rows_fpl[0][2], rows_transfer[0][1], rows_fpl[0][0],
                rows_fpl[0][1])
            print(data_tuple)
            cursor.execute(sql_insert_into_clubs, data_tuple)
            cnx.commit()
        except sqlite3.Error as error:

            print("Error while creating a sqlite table", error)
        except Exception as e:
            print(e)
    if (cnx): cnx.close()


cursor = connection.cursor()
cursor.execute(sqlite_create_table_players_transfermarkt_singles)
connection.commit()

insert_into_players_transfermarkt_singles()
connection.commit()

cursor.execute(sqlite_delete_table_players_transfermarkt_fpl)
connection.commit()

cursor.execute(sqlite_create_table_players_transfermarkt_fpl)
connection.commit()

insert_into_players_transfermarkt_fpl()
connection.commit()

insert_into_players_transfermarkt_fpl_extra_time()
connection.commit()

insert_into_players_transfermarkt_fpl_singles('Thiago', 'Thiago', 'Alcantara do Nascimento')
connection.commit()
insert_into_players_transfermarkt_fpl_singles('Nélson Semedo', 'Nelson', 'Cabral Semedo')
connection.commit()
insert_into_players_transfermarkt_fpl_singles('Kepa', 'Kepa', 'Arrizabalaga')
connection.commit()
insert_into_players_transfermarkt_fpl_singles('John Mikel Obi', 'John Obi', 'Mikel')
connection.commit()
insert_into_players_transfermarkt_fpl_singles('Heung-min Son', 'Heung-Min', 'Son')
connection.commit()
insert_into_players_transfermarkt_fpl_singles('Ederson', 'Ederson', 'Santana de Moraes')
connection.commit()
insert_into_players_transfermarkt_fpl_singles('Dionatan Teixeira', 'Dionatan do Nascimento', 'Teixeira')
connection.commit()

connection.close()
