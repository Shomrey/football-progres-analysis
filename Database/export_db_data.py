import os
import sqlite3 as sql
import pandas as pd

# var_nam = (sql_table, export_file_name)

player_guid = ('players', 'players_guid.csv')
position = ('position', 'position.csv')
player_statistics = ('player_statistics', 'unified_players.csv')
clubs = ('clubs', os.path.join('csv_transfermarkt', 'Clubs.csv'))
player_transfermarkt = ('players_transfermarkt', os.path.join("csv_transfermarkt", "Players.csv"))
player_values = ('player_values', os.path.join("csv_transfermarkt", "Values.csv"))
player_transfermarkt_fpl = ('players_transfermarkt_fpl', 'players_transfermarkt_fpl.csv')

list_of_tables = [player_guid, position, player_statistics, clubs, player_transfermarkt, player_values, player_transfermarkt_fpl]

connection = sql.connect("fpa-database-fix.db")

for table in list_of_tables:
    tmp_df = pd.read_sql_query('SELECT * FROM {}'.format(table[0]), connection)
    tmp_df.to_csv(table[1], index=False, index_label=True)
    print('Exported {}'.format(table[0]))

connection.close()