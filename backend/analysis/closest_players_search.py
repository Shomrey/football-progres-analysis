import sqlite3
import pandas as pd
from scipy.spatial import distance


def get_index_for_player_guid(players, guid):
    player_id = players[(players['guid'] == guid)].index
    print(player_id)
    return player_id

def get_player_row(player_data, index):
    return player_data.iloc[index, :]


def get_distances_for_player(player_data, player):
    distances = dict()
    for index, row in player_data.iterrows():
        dist = distance.euclidean(player, row)
        distances[index] = dist
    return distances


def sort_dict_by_value(distances):
    return sorted(distances.items(), key=lambda x: x[1])


def divide_dataframe(players):
    names = players.iloc[:, [0, 1, 2, -2, -1]]
    stats = players.iloc[:, 3:-2]
    return names, stats


def find_closest_players_for_player_in_season(cnx, neighbours_season, players_df, guid, n=5):
    counter = 0
    index = get_index_for_player_guid(players_df, guid)

    possible_neighbours = pd.read_sql_query("SELECT * from player_statistics as p " + \
                                            "WHERE p.year = {}".format(neighbours_season), cnx)

    possible_neighbours_names, possible_neighbours_stats = divide_dataframe(possible_neighbours)
    names, stats = divide_dataframe(players_df)

    try:
        index = index.tolist()[0]
    except:
        return dict()

    player_data = names.iloc[index, :]
    print(player_data)

    player_row = get_player_row(stats, index)
    distances = get_distances_for_player(possible_neighbours_stats, player_row)
    distances = sort_dict_by_value(distances)
    neighbours = dict()

    for i in range(1, len(distances)):
        ind = distances[i][0]
        player_data = (possible_neighbours_names.iloc[ind, :])
        neighbours[ind] = player_data
        counter = counter + 1
        if counter == n:
            return neighbours


def get_closest_players_dataframe(players_with_values, closest_players):
    guids = []
    columns = players_with_values.columns
    closest_players_df = pd.DataFrame(columns=columns)

    for a in closest_players.values():
        guid = a.guid
        player_data = players_with_values[(players_with_values['guid'] == guid) & (players_with_values['year'] == 2016) ]
        for i, j in player_data.iterrows():
            if guid in guids:
                pass
            else:
                guids.append(guid)
                closest_players_df = closest_players_df.append(j)

    return closest_players_df