from flask import Blueprint, request
import sqlite3
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from . import prediction
from . import data

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
    return perspective_forwards_df.to_json(orient='records'), 200
