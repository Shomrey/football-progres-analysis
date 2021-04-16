import database_setup_utils as dsu
import pandas as pd

connection = dsu.create_empty_database()

players_table_values = pd.read_csv('players_guid.csv')
position_table_values = pd.read_csv('position.csv')
player_statistics_table_values = pd.read_csv('unified_players.csv')

players_table_values.to_sql(name='players', con=connection, index_label='id', index=False)
position_table_values.to_sql(name='position', con=connection, index_label='id', index=False)
player_statistics_table_values.to_sql(name='player_statistics', con=connection, index_label=('guid', 'year'), index=False)

connection.close()

