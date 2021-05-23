from . import prediction
import sqlite3
import pandas as pd


forwards_training_parameters = ['bps', 'influence', 'goals_scored',
                                'ict_index', 'total_points']
wingers_training_parameters = ['threat', 'goals_scored', 'ict_index',
                               'total_points', 'influence', 'bonus']
midfielders_training_parameters = ['ict_index', 'assists', 'creativity',
                                   'selected_by_percent', 'influence', 'total_points']
target = 'player_value'
cnx = sqlite3.connect('../Database/fpa-database.db', check_same_thread=False)


players_with_values = prediction.get_players_with_values(cnx)

forwards = prediction.get_players_by_position(players_with_values, 'forwards')
wingers = prediction.get_players_by_position(players_with_values, 'wingers')
midfielders = prediction.get_players_by_position(players_with_values, 'midfielders')

prediction.predict_value(forwards, forwards_training_parameters, target, result_column_name='predicted_value')
prediction.predict_value(wingers, wingers_training_parameters, target, result_column_name='predicted_value')
prediction.predict_value(midfielders, wingers_training_parameters, target, result_column_name='predicted_value')


def get_players_stats(season):
    global cnx
    players_stats = pd.read_sql_query("SELECT * from player_statistics as p " + \
                                           "WHERE p.year = {}".format(season), cnx)
    player_names = players_stats.iloc[:, [0, 1, 2, -2, -1]]
    player_data = players_stats.iloc[:, 3:-2]
    return players_stats, player_names, player_data


def get_guid_for_player(dataframe, first_name, second_name):
    try:
        player = players_with_values[(dataframe['first_name'] == first_name) & (dataframe['second_name'] == second_name)]
        player_guid = player['guid'].values[0]
        return player_guid
    except:
        raise PlayerNotFound()

class PlayerNotFound(Exception):
    pass
