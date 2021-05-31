import pandas as pd
from sklearn.linear_model import LinearRegression

FORWARDS = 'forwards'
WINGERS = 'wingers'
MIDFIELDERS = 'midfielders'
BACK_DEFENDERS = 'back-defenders'
CENTER_DEFENDERS = 'center-defenders'
GOALKEEPERS = 'goalkeepers'
VALID_POSITIONS = [FORWARDS, WINGERS, MIDFIELDERS, BACK_DEFENDERS, CENTER_DEFENDERS, GOALKEEPERS]


def get_perspective_players_dataframe(data, columns, min_percent, max_percent):
    perspective_players = get_players_with_higher_predicted_value(data, min_percent, max_percent)
    print(perspective_players)
    perspective_players_df = pd.DataFrame(columns=columns)

    for k in perspective_players.keys():
        perspective_players_df = perspective_players_df.append(perspective_players[k])

    perspective_players_df = perspective_players_df[perspective_players_df['minutes'] > 0]
    return perspective_players_df


def get_players_with_higher_predicted_value(data, min_precent, max_percent):
    players_with_higher_than_actual_value = dict()
    for index, row in data.iterrows():
        if row['predicted_value_diff_percent'] > min_precent and row['predicted_value_diff_percent'] < 400:
            i = row['guid']
            if i in players_with_higher_than_actual_value.keys():
                pass
            players_with_higher_than_actual_value[i] = row
            print(row['first_name'], row['second_name'], row['guid'])
    return players_with_higher_than_actual_value


def get_player_for_given_season(players, season, max_age=None, min_age=None, max_value=None, min_value=None):
    season = (players['year'] == season)
    min_age = (players['age'] >= min_age) if min_age else True
    max_age = (players['age'] <= max_age) if max_age else True
    min_value = (players['max_value'] >= min_value) if min_value else True
    max_value = (players['max_value'] <= max_value) if max_value else True

    return players[season & min_age & max_age & min_value & max_value]


def fit_linear_regression(data, training_parameters, target):
    mlr = LinearRegression()
    data_fitted = mlr.fit(data[training_parameters], data[target])
    return data_fitted


def get_players_with_values(cnx):
    players_with_values = pd.read_sql_query("SELECT * from players as p " + \
                                            "JOIN players_transfermarkt_fpl as ptf on ptf.player_id_fpl = p.guid " + \
                                            "JOIN players_transfermarkt_singles as pts on pts.id = ptf.player_id_transfermarkt " +
                                            "JOIN player_statistics as ps on ps.guid = p.guid " +
                                            "JOIN player_values as pv on pv.transfermarkt_player_id = pts.id " +
                                            "WHERE strftime('%Y',pv.date_stamp) = ps.year", cnx)

    players_with_values = players_with_values.dropna(axis=1)
    get_age = lambda x: (x['year']) - int((x["date_of_birth"].split(" ")[0].split('-')[0]))
    players_with_values["age"] = players_with_values.apply(get_age, axis=1)

    indexes = players_with_values[players_with_values['player_value'] < 10000].index
    players_with_values.drop(index=indexes, inplace=True)

    players_with_values = players_with_values.loc[:,~players_with_values.columns.duplicated()]
    return players_with_values


def get_players_by_position(players_with_values, position):
    forwards = players_with_values[(players_with_values['player_position'] ==  'Centre-Forward') |
                                   (players_with_values['player_position'] ==  'Second Striker')]

    wingers = players_with_values[(players_with_values['player_position'] ==  'Left Winger') |
                                  (players_with_values['player_position'] ==  'Right Winger')]

    midfielders = players_with_values[(players_with_values['player_position'] ==  'Attacking Midfield') |
                                      (players_with_values['player_position'] ==  'Defensive Midfield') |
                                      (players_with_values['player_position'] ==  'Central Midfield') |
                                      (players_with_values['player_position'] ==  'Left Midfield') |
                                      (players_with_values['player_position'] ==  'Right Midfield')
                                      ]

    center_defenders = players_with_values[(players_with_values['player_position'] ==  'Centre-Back')
    ]

    back_defenders = players_with_values[(players_with_values['player_position'] ==  'Left-Back') |
                                         (players_with_values['player_position'] ==  'Right-Back')
                                         ]

    goalkeepers = players_with_values[(players_with_values['player_position'] ==  'Goalkeeper')]

    result = None
    if position == FORWARDS:
        result = forwards
    elif position == WINGERS:
        result = wingers
    elif position == MIDFIELDERS:
        result = midfielders
    elif position == BACK_DEFENDERS:
        result = back_defenders
    elif position == CENTER_DEFENDERS:
        result = center_defenders
    elif position == GOALKEEPERS:
        result = goalkeepers
    return result
    # corr = forwards.corr()
    # forwards_corr = corr['player_value']
    # forwards_corr = forwards_corr.sort_values(ascending=False)
    # print(forwards_corr)
    # forwards_corr.keys()


def predict_value(data, training_parameters, target, result_column_name):
    fit = fit_linear_regression(data, training_parameters , target)
    predicted_value = fit.predict(data[training_parameters])
    data[result_column_name] = predicted_value
    get_predicted_value_diff(data, result_column_name, target)


def get_predicted_value_diff(data, result_column_name, target):
    predicted_value_diff = lambda x: (x[result_column_name] - x[target])
    predicted_value_diff_percent = lambda x: ((x[result_column_name] - x[target]) / (x[target])) * 100

    data[result_column_name + '_diff'] = data.apply(predicted_value_diff, axis=1)
    data[result_column_name + '_diff_percent'] = data.apply(predicted_value_diff_percent, axis=1)
