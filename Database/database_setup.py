import Database.database_setup_utils as dsu
import pandas as pd

connection = dsu.create_empty_database()

players_table_values = pd.read_csv('players_guid.csv')
position_table_values = pd.read_csv('position.csv')
player_statistics_table_values = pd.read_csv('unified_players.csv')

players_table_values.to_sql(name='players', con=connection, index_label='id', index=False)
position_table_values.to_sql(name='position', con=connection, index_label='id', index=False)
player_statistics_table_values.to_sql(name='player_statistics', con=connection, index_label=('guid', 'year'), index=False)

sqlite_create_table_clubs = ''' CREATE TABLE IF NOT EXISTS clubs (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            url text NOT NULL,
                                            number_of_footballers integer NOT NULL,
                                            club_value text NOT NULL
                                        ); '''

sqlite_create_table_values = ''' CREATE TABLE IF NOT EXISTS player_values (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            transfermarkt_player_id text NOT NULL,
                                            date_stamp timestamp  integer NOT NULL,
                                            player_value integer NOT NULL,
                                            player_club text NOT NULL,
                                            FOREIGN KEY (transfermarkt_player_id) REFERENCES players_transfermarkt (id) ON DELETE CASCADE
                                        ); '''

sqlite_create_table_players_transfermarkt = ''' CREATE TABLE IF NOT EXISTS players_transfermarkt (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            date_of_birth timestamp NOT NULL,
                                            player_position text  integer NOT NULL,
                                            nationality text NOT NULL,
                                            current_value integer NOT NULL,
                                            url text NOT NULL,
                                            current_club_id NOT NULL,
                                            FOREIGN KEY (current_club_id) REFERENCES clubs (id) ON DELETE CASCADE
                                       
                                        ); '''

cursor = connection.cursor()
cursor.execute(sqlite_create_table_clubs)
cursor.execute(sqlite_create_table_values)
cursor.execute(sqlite_create_table_players_transfermarkt)
connection.commit()

connection.close()

