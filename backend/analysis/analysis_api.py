from flask import Blueprint, request
import sqlite3
import pandas as pd
import json
from . import prediction
from . import data
from . import closest_players_search

app_analysis = Blueprint("app_login", __name__)

cnx = sqlite3.connect('../Database/fpa-database.db', check_same_thread=False)


@app_analysis.route('/perspective/<position>', methods=["GET"])
def get_perspective_players_by_position(position):
    if position not in prediction.VALID_POSITIONS:
        return 'Bad request, valid positions are {}'.format(prediction.VALID_POSITIONS), 400

    season = request.args.get('season', default=2020, type=int)
    max_age = request.args.get('max_age', default=24, type=int)

    if position == prediction.FORWARDS:
        players_by_position = data.forwards
    elif position == prediction.WINGERS:
        players_by_position = data.wingers
    elif position == prediction.MIDFIELDERS:
        players_by_position = data.midfielders

    perspective_players = prediction.get_player_for_given_season(players_by_position, season=season, max_age=max_age)
    perspective_players_sorted = perspective_players.sort_values('predicted_value_diff_percent', ascending=False)

    columns = perspective_players.columns
    perspective_forwards_df = prediction.get_perspective_players_dataframe(perspective_players, columns, 4, 400)

    perspective = json.loads(perspective_forwards_df.to_json(orient='records'))
    results = dict()
    results['players'] = perspective

    return json.dumps(results), 200


@app_analysis.route('/closest/<int:guid>', methods=["GET"])
def get_closest_players(guid):
    '''Returns closest players to player with given guid in season neighseason
    Moreover, it is also retuned higest value of one of closest players
    in period since neighseason and 2 years after as predicted value'''
    try:
        season = request.args.get('season', default=2020, type=int)
        neighbour_season = request.args.get('neighseason', default=2016, type=int)
        players_stats, _, _ = data.get_players_stats(season)

        closest_players = closest_players_search.find_closest_players_for_player_in_season(cnx, neighbour_season, players_stats, guid=guid)
        closest_players_df = closest_players_search.get_closest_players_dataframe(data.players_with_values, closest_players)
        print(closest_players_df)
        print(closest_players_df['guid'])
    except data.PlayerNotFound:
        print('Player not found')
    except:
        return 'Bad request', 400

    columns = ['guid', 'date_stamp', 'player_value', 'player_club']
    closest_players_values = pd.DataFrame(columns=columns)

    guids = closest_players_df['guid'].values
    guids = tuple(guids)

    player_vals = pd.read_sql_query("""SELECT ftp.player_id_fpl as guid, p.date_stamp, p.player_value, p.player_club from player_values as p 
                                        JOIN players_transfermarkt_fpl as ftp on ftp.player_id_transfermarkt = p.transfermarkt_player_id
                                                WHERE ftp.player_id_fpl IN {}
                                                AND p.date_stamp BETWEEN '{}-01-01 00:00:01' AND '{}-12-31 23:59:59'""".format(guids, neighbour_season, neighbour_season+2), cnx)

    closest_players_values = closest_players_values.append(player_vals)
    max_value = (closest_players_values['player_value'].max())
    max_value_player = (closest_players_values[closest_players_values['player_value'] == max_value].iloc[0])

    closest = json.loads(closest_players_df.to_json(orient='records'))
    results = dict()
    results['players'] = closest
    results['guid'] = max_value_player['guid']
    results['predicted_value'] = max_value_player['player_value']
    results['date_stamp'] = max_value_player['date_stamp']
    print(max_value_player)
    return json.dumps(results), 200


@app_analysis.route('/player')
def get_guid_por_player():
    first_name = request.args.get('first', type=str)
    second_name = request.args.get('second', type=str)
    try:
        guid = data.get_guid_for_player(data.players_with_values, first_name, second_name)
    except:
        return 'Bad request', 400

    return 'Player: {} {} GUID: {} '.format(first_name, second_name, guid), 200