from . import prediction
import sqlite3

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




