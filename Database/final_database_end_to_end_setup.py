import os
import sqlite3

from unidecode import unidecode

import Database.database_setup_utils as dsu
import pandas as pd

connection = dsu.create_empty_database()

players_table_values = pd.read_csv('players_guid.csv')
position_table_values = pd.read_csv('position.csv')
player_statistics_table_values = pd.read_csv('unified_players.csv')

players_table_values.to_sql(name='players', con=connection, index_label='id', index=False)
position_table_values.to_sql(name='position', con=connection, index_label='id', index=False)
player_statistics_table_values.to_sql(name='player_statistics', con=connection, index_label=('guid', 'year'),
                                      index=False)

sqlite_create_table_clubs = ''' CREATE TABLE IF NOT EXISTS clubs (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            club_name text NOT NULL,
                                            url text NOT NULL,
                                            number_of_footballers integer NOT NULL,
                                            club_value text NOT NULL,
                                            season integer NOT NULL
                                        ); '''

sqlite_create_table_values = ''' CREATE TABLE IF NOT EXISTS player_values (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            transfermarkt_player_id text NOT NULL,
                                            date_stamp timestamp  integer NOT NULL,
                                            player_value integer NOT NULL,
                                            player_club text NOT NULL,
                                            player_url text NOT NULL,
                                            FOREIGN KEY (transfermarkt_player_id) REFERENCES players_transfermarkt_singles (id) ON DELETE CASCADE
                                        ); '''

sqlite_create_table_players_transfermarkt = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            player_name text NOT NULL,
                                            current_value integer NOT NULL,
                                            url text NOT NULL,
                                            current_club_id integer NOT NULL,
                                            season integer NOT NULL,
                                            global_transfermarkt_id integer not null,
                                            FOREIGN KEY (current_club_id) REFERENCES clubs (id) ON DELETE CASCADE,
                                            FOREIGN KEY (global_transfermarkt_id) REFERENCES players_transfermarkt_singles (id) ON DELETE CASCADE
                                        ); '''

sqlite_create_table_players_transfermarkt_singles = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt_singles (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            player_name text NOT NULL,
                                            date_of_birth timestamp NOT NULL,
                                            player_position text  integer NOT NULL,
                                            nationality text NOT NULL
                                        ); '''

sqlite_create_table_players_transfermarkt_fpl = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt_fpl (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            player_id_transfermarkt integer NOT NULL,
                                            player_id_fpl integer NOT NULL,
                                            player_name_transfermarkt text not null,
                                            first_name text not null,
                                            second_name text non null,
                                            FOREIGN KEY (player_id_transfermarkt) REFERENCES players_transfermarkt_singles (id) ON DELETE CASCADE,
                                            FOREIGN KEY (player_id_fpl) REFERENCES players (guid) ON DELETE CASCADE
                                        ); '''


def insert_into_clubs():
    seasons = ['2015', '2016', '2017', '2018', '2019', '2020']
    for season in seasons:
        filename = os.path.join("csv_transfermarkt", "Clubs_" + season + ".csv")
        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            try:
                sqlite_connection = sqlite3.connect("fpa-database-fix.db")
                cursor = sqlite_connection.cursor()

                sql_insert_into_clubs = '''INSERT INTO clubs
                                              (  club_name, url,number_of_footballers, club_value, season)
                                               VALUES
                                              (?, ?, ?,?,?)'''
                data_tuple = (
                    row['club_name'], row['reference'], row['number_of_footballers'], row['total_value'], int(season))
                cursor.execute(sql_insert_into_clubs, data_tuple)
                sqlite_connection.commit()
            except sqlite3.Error as error:
                print("Error while insert_into_clubs", error)
            finally:
                if (sqlite_connection):
                    sqlite_connection.close()


def insert_into_players_transfermarkt():
    seasons = ['2015', '2016', '2017', '2018', '2019', '2020']
    for season in seasons:
        filename = os.path.join("csv_transfermarkt", "Players_" + season + ".csv")
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            try:

                sqlite_connection = sqlite3.connect("fpa-database-fix.db")
                cursor = sqlite_connection.cursor()

                # logika !!!!!! wsadzam do singles jeśli nie ma

                id_from_player_transfer_markt_singles = select_id_from_players_transfermarkt_singles_by_player_name(
                    row['name_and_surname'])

                if id_from_player_transfer_markt_singles is None:
                    sql_insert_into_players_transfermarkt_singles = '''INSERT INTO players_transfermarkt_singles
                                                  (player_name, date_of_birth, player_position, nationality)
                                                   VALUES
                                                  (?, ?, ?, ?)'''
                    data_tuple = (
                        row['name_and_surname'], row['date_of_birth'], row['position'], row['country'])
                    cursor.execute(sql_insert_into_players_transfermarkt_singles, data_tuple)
                    sqlite_connection.commit()

                    # teraz już będzie !!!!!
                    id_from_player_transfer_markt_singles = select_id_from_players_transfermarkt_singles_by_player_name(
                        row['name_and_surname'])

                sql_insert_into_clubs = '''INSERT INTO players_transfermarkt
                                              (player_name, current_value , url, current_club_id, season, global_transfermarkt_id)
                                               VALUES
                                              (?, ?, ?, ?, ?, ?)'''
                club_id = select_club_id_from_clubs_by_url(
                    row['club_reference'].split("https://www.transfermarkt.com")[1])

                data_tuple = (
                    row['name_and_surname'], row['market_value'],
                    row['href'], club_id, int(season), id_from_player_transfer_markt_singles)
                cursor.execute(sql_insert_into_clubs, data_tuple)
                sqlite_connection.commit()
            except sqlite3.Error as error:
                print("Error while creating a sqlite table", error)
            finally:
                if (sqlite_connection):
                    sqlite_connection.close()


def insert_into_player_values():
    filename = os.path.join("csv_transfermarkt", "Values.csv")
    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        try:
            sqlite_connection = sqlite3.connect("fpa-database-fix.db")
            cursor = sqlite_connection.cursor()

            sql_insert_into_clubs = '''INSERT INTO player_values
                                          (transfermarkt_player_id,date_stamp,player_value,player_club, player_url)
                                           VALUES
                                          (?, ?, ?,?, ?)'''
            player_id = select_player_id_from_players_transfermarkt_by_url(
                row['player_reference'].split("https://www.transfermarkt.com")[1])
            player_url = row['player_reference'].split("https://www.transfermarkt.com")[1]
            data_tuple = (player_id, row['date'], row['value'], row['club'], player_url)
            cursor.execute(sql_insert_into_clubs, data_tuple)
            sqlite_connection.commit()
        except sqlite3.Error as error:

            print("Error while insert_into_player_values", error)
        except Exception as e:
            print(row)
            print(e)
            # blad wynika z czytania linijka z nagłowkiem - niegrozny, ale do poprawy #TODO
        finally:
            if (sqlite_connection):
                sqlite_connection.close()


def insert_into_player_values_missing():
    filename = os.path.join("csv_transfermarkt", "Values_Missing.csv")
    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        try:

            sqlite_connection = sqlite3.connect("fpa-database-fix.db")
            cursor = sqlite_connection.cursor()

            sql_insert_into_clubs = '''INSERT INTO player_values
                                          (transfermarkt_player_id,date_stamp,player_value,player_club, player_url)
                                           VALUES
                                          (?, ?, ?,?, ?)'''
            player_id = select_player_id_from_players_transfermarkt_by_url(
                row['player_reference'].split("https://www.transfermarkt.com")[1])
            player_url = row['player_reference'].split("https://www.transfermarkt.com")[1]
            data_tuple = (player_id, row['date'], row['value'], row['club'], player_url)
            cursor.execute(sql_insert_into_clubs, data_tuple)
            sqlite_connection.commit()
        except sqlite3.Error as error:

            print("Error while insert_into_player_values_missing", error)
        except Exception as e:
            print(row)
            print(e)
            # blad wynika z czytania linijka z nagłowkiem - niegrozny, ale do poprawy #TODO
        finally:
            if (sqlite_connection):
                sqlite_connection.close()


def select_club_id_from_clubs_by_url(url):
    sqlite_connection = sqlite3.connect("fpa-database-fix.db")
    cursor = sqlite_connection.cursor()
    sql_insert_into_clubs = '''SELECT  id from clubs where url = ?'''
    data_tuple = (url,)
    cursor.execute(sql_insert_into_clubs, data_tuple)

    rows = cursor.fetchall()
    sqlite_connection.close()

    for row in rows:
        return row[0]


def select_id_from_players_transfermarkt_singles_by_player_name(player_name):
    sqlite_connection = sqlite3.connect("fpa-database-fix.db")
    cursor = sqlite_connection.cursor()
    sql_insert_into_clubs = '''SELECT  id from players_transfermarkt_singles where player_name = ?'''
    data_tuple = (player_name,)
    cursor.execute(sql_insert_into_clubs, data_tuple)

    rows = cursor.fetchall()
    sqlite_connection.close()

    if len(rows) == 0:
        return None
    if len(rows) != 1:
        print("UWAGA NIEJEDNOZNACZNE PLAYER NAME")
    for row in rows:
        return row[0]


def select_all_players_names():
    sqlite_connection = sqlite3.connect("fpa-database-fix.db")
    cursor = sqlite_connection.cursor()
    sql_insert_into_clubs = '''select player_name from players_transfermarkt group by player_name'''
    cursor.execute(sql_insert_into_clubs)
    rows = cursor.fetchall()
    sqlite_connection.close()

    return rows


def select_player_id_from_players_transfermarkt_by_url(url):
    sqlite_connection = sqlite3.connect("fpa-database-fix.db")
    cursor = sqlite_connection.cursor()
    sql_insert_into_clubs = '''SELECT  id from players_transfermarkt where url = ?'''
    data_tuple = (url,)
    cursor.execute(sql_insert_into_clubs, data_tuple)

    rows = cursor.fetchall()
    sqlite_connection.close()

    for row in rows:
        return row[0]


sqlite_create_table_values_transfermarkt = ''' CREATE TABLE IF NOT EXISTS player_values_transfermarkt (
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

            print("Error while insert_into_player_values_transfermarkt", error)
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

                    print("Error while insert_into_players_transfermarkt_fpl", error)
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

                        print("Error while insert_into_players_transfermarkt_fpl_extra_time", error)
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

            print("Error insert_into_players_transfermarkt_fpl_singles", error)
        except Exception as e:
            print(e)
    if (cnx): cnx.close()


cursor = connection.cursor()
cursor.execute(sqlite_create_table_clubs)
cursor.execute(sqlite_create_table_players_transfermarkt_singles)
cursor.execute(sqlite_create_table_values)
cursor.execute(sqlite_create_table_players_transfermarkt)
cursor.execute(sqlite_create_table_players_transfermarkt_fpl)

connection.commit()

insert_into_clubs()
connection.commit()

insert_into_players_transfermarkt()
connection.commit()
insert_into_player_values()
connection.commit()
insert_into_player_values_missing()
connection.commit()

cursor.execute(sqlite_create_table_values_transfermarkt)
connection.commit()

insert_into_player_values_transfermarkt()
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
