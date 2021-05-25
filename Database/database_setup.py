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
                                            FOREIGN KEY (transfermarkt_player_id) REFERENCES players_transfermarkt (id) ON DELETE CASCADE
                                        ); '''

sqlite_create_table_players_transfermarkt = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            player_name text NOT NULL,
                                            date_of_birth timestamp NOT NULL,
                                            player_position text  integer NOT NULL,
                                            nationality text NOT NULL,
                                            current_value integer NOT NULL,
                                            url text NOT NULL,
                                            current_club_id integer NOT NULL,
                                            season integer NOT NULL,
                                            FOREIGN KEY (current_club_id) REFERENCES clubs (id) ON DELETE CASCADE
                                       
                                        ); '''

sqlite_create_table_players_transfermarkt_fpl = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt_fpl (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            player_id_transfermarkt integer NOT NULL,
                                            player_id_fpl integer NOT NULL,
                                            FOREIGN KEY (player_id_transfermarkt) REFERENCES players_transfermarkt (id) ON DELETE CASCADE
                                        ); '''


#    FOREIGN KEY (player_id_fpl) REFERENCES players (guid) ON DELETE CASCADE


def insert_into_clubs():
    seasons = ['2015', '2016', '2017', '2018', '2019', '2020']
    for season in seasons:
        filename = os.path.join("csv_transfermarkt", "Clubs_" + season + ".csv")
        df = pd.read_csv(filename)

        for index, row in df.iterrows():
            try:
                sqlite_connection = sqlite3.connect("fpa-database.db")
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
                print("Error while creating a sqlite table", error)
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
                sqlite_connection = sqlite3.connect("fpa-database.db")
                cursor = sqlite_connection.cursor()

                sql_insert_into_clubs = '''INSERT INTO players_transfermarkt
                                              (player_name, date_of_birth,  player_position, nationality, current_value , url, current_club_id, season)
                                               VALUES
                                              (?, ?, ?,?, ?, ?, ?, ?)'''
                club_id = select_club_id_from_clubs_by_url(
                    row['club_reference'].split("https://www.transfermarkt.com")[1])

                data_tuple = (
                    row['name_and_surname'], row['date_of_birth'], row['position'], row['country'], row['market_value'],
                    row['href'], club_id, int(season))
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
            sqlite_connection = sqlite3.connect("fpa-database.db")
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

            print("Error while creating a sqlite table", error)
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
            sqlite_connection = sqlite3.connect("fpa-database.db")
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

            print("Error while creating a sqlite table", error)
        except Exception as e:
            print(row)
            print(e)
            # blad wynika z czytania linijka z nagłowkiem - niegrozny, ale do poprawy #TODO
        finally:
            if (sqlite_connection):
                sqlite_connection.close()


def select_club_id_from_clubs_by_url(url):
    sqlite_connection = sqlite3.connect("fpa-database.db")
    cursor = sqlite_connection.cursor()
    sql_insert_into_clubs = '''SELECT  id from clubs where url = ?'''
    data_tuple = (url,)
    cursor.execute(sql_insert_into_clubs, data_tuple)

    rows = cursor.fetchall()
    sqlite_connection.close()

    for row in rows:
        return row[0]

def select_all_players_names():
    sqlite_connection = sqlite3.connect("fpa-database.db")
    cursor = sqlite_connection.cursor()
    sql_insert_into_clubs = '''select player_name from players_transfermarkt group by player_name'''
    cursor.execute(sql_insert_into_clubs)
    rows = cursor.fetchall()
    sqlite_connection.close()

    return rows




def select_player_id_from_players_transfermarkt_by_url(url):
    sqlite_connection = sqlite3.connect("fpa-database.db")
    cursor = sqlite_connection.cursor()
    sql_insert_into_clubs = '''SELECT  id from players_transfermarkt where url = ?'''
    data_tuple = (url,)
    cursor.execute(sql_insert_into_clubs, data_tuple)

    rows = cursor.fetchall()
    sqlite_connection.close()

    for row in rows:
        return row[0]




cursor = connection.cursor()
cursor.execute(sqlite_create_table_clubs)
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
# insert_into_players_transfermarkt_fpl()

connection.close()
