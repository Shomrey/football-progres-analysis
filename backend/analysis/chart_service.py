import os
import sqlite3

import matplotlib.dates as mdates
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

import numpy as np

from Database.database_constants import DATABASE_NAME

CHARTS_DIRECTORY = os.path.join("..", "dynamic_charts")
PATH_TO_CHARTS_DIR = '../../dynamic_charts/'

def get_player_value_chart(guid):
    cnx = sqlite3.connect(os.path.join("..", "Database", DATABASE_NAME))

    cur = cnx.cursor()
    cur.execute(
        """select pvt.date_stamp, pvt.player_value, pvt.player_club 
           from player_values_transfermarkt pvt
           where pvt.transfermarkt_player_id = (select player_id_transfermarkt from players_transfermarkt_fpl where player_id_fpl = ?) 
           order by pvt.date_stamp""",
        (int(guid),))
    rows = cur.fetchall()
    print(rows)

    origin = []
    b = []
    clubs = []
    for row in rows:
        origin.append(row[0])
        b.append(row[1] / 10 ** 6)
        clubs.append(row[2])

    labels, index = np.unique(clubs, return_inverse=True)

    a = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in origin]

    x = matplotlib.dates.date2num(a)
    formatter = matplotlib.dates.DateFormatter('%Y-%m')

    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)

    axes.xaxis.set_major_formatter(formatter)
    plt.setp(axes.get_xticklabels(), rotation=45)

    sc = axes.scatter(x, b, c=index)
    axes.legend(sc.legend_elements()[0], labels)
    plt.ylabel("Market value [mln euro]")
    plt.plot(x, b, linestyle='dashed')
    file_name = "{}.png".format(get_player_surname(guid))
    path = PATH_TO_CHARTS_DIR + file_name
    abs_path = os.path.abspath(path)
    plt.savefig(os.path.join("../dynamic_charts/" + file_name))
    plt.show()
    if (cnx): cnx.close()
    return abs_path


def get_player_surname(guid):
    cnx = sqlite3.connect(os.path.join("..", "Database", DATABASE_NAME))

    cur = cnx.cursor()
    cur.execute(
        """select second_name
           from players where guid = ?""",
        (int(guid),))
    rows = cur.fetchall()
    if (cnx): cnx.close()
    return rows[0][0]


def get_player_transfermarkt_id_by_guid(guid):
    cnx = sqlite3.connect(os.path.join("..", "Database", DATABASE_NAME))

    cur = cnx.cursor()
    cur.execute(
        """select player_id_transfermarkt
           from players_transfermarkt_fpl
           where player_id_fpl = ?""",
        (int(guid),))
    rows = cur.fetchall()
    if (cnx): cnx.close()
    return rows[0][0]


def get_players_comparison_value_chart(guid1, guid2):
    cnx = sqlite3.connect(os.path.join("..", "Database", DATABASE_NAME))

    cur = cnx.cursor()
    cur.execute(
        """select pvt.date_stamp, pvt.player_value, pvt.player_club 
           from player_values_transfermarkt pvt
           where pvt.transfermarkt_player_id = (select player_id_transfermarkt from players_transfermarkt_fpl where player_id_fpl = ?) 
           order by pvt.date_stamp""",
        (int(guid1),))
    rows_1 = cur.fetchall()

    cur.execute(
        """select pvt.date_stamp, pvt.player_value, pvt.player_club 
           from player_values_transfermarkt pvt
           where pvt.transfermarkt_player_id = (select player_id_transfermarkt from players_transfermarkt_fpl where player_id_fpl = ?) 
           order by pvt.date_stamp""",
        (int(guid2),))
    rows_2 = cur.fetchall()

    origin1 = []
    b1 = []
    clubs1 = []
    for row in rows_1:
        origin1.append(row[0])
        b1.append(row[1] / 10 ** 6)
        clubs1.append(row[2])

    origin2 = []
    b2 = []
    clubs2 = []
    for row in rows_2:
        origin2.append(row[0])
        b2.append(row[1] / 10 ** 6)
        clubs2.append(row[2])

    # origin = origin1.append(origin2)
    b = b1 + b2
    clubs = clubs1 + clubs2

    labels, index = np.unique(clubs, return_inverse=True)

    a1 = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in origin1]
    a2 = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in origin2]

    x1 = matplotlib.dates.date2num(a1)
    x2 = matplotlib.dates.date2num(a2)

    formatter = matplotlib.dates.DateFormatter('%Y-%m')

    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)

    axes.xaxis.set_major_formatter(formatter)
    plt.setp(axes.get_xticklabels(), rotation=45)
    x = matplotlib.dates.date2num(a1 + a2)
    sc = axes.scatter(x, b, c=index)
    legend1 = axes.legend(sc.legend_elements()[0], labels)
    plt.ylabel("Market value [mln euro]")

    first, = axes.plot(x1, b1, linestyle='dashed')
    second, = axes.plot(x2, b2, linestyle='dashed')
    first_tuple = get_fpl_first_name_and_last_name_from_transfermarkt_id(get_player_transfermarkt_id_by_guid(guid1))
    second_tuple = get_fpl_first_name_and_last_name_from_transfermarkt_id(get_player_transfermarkt_id_by_guid(guid2))
    axes.legend([first, second], [first_tuple[0] + ' ' + first_tuple[1], second_tuple[0] + ' ' + second_tuple[1]],
                loc='lower center')
    # Manually add the first legend back
    axes.add_artist(legend1)

    file_name = "{}_{}.png".format(get_player_surname(guid1), get_player_surname(guid2))
    path = PATH_TO_CHARTS_DIR + file_name
    abs_path = os.path.abspath(path)
    plt.savefig(os.path.join("../dynamic_charts/" + file_name))
    plt.show()
    if (cnx): cnx.close()
    return abs_path


def get_fpl_first_name_and_last_name_from_transfermarkt_id(transfermarkt_id):
    sqlite_connection = sqlite3.connect(os.path.join("..", "Database", DATABASE_NAME))
    cursor = sqlite_connection.cursor()
    sql_select = '''select first_name, second_name, guid from players where guid =
                            (select player_id_fpl from players_transfermarkt_fpl where player_id_transfermarkt = ?);'''
    data_tuple = (transfermarkt_id,)
    cursor.execute(sql_select, data_tuple)

    rows = cursor.fetchall()
    sqlite_connection.close()
    # TODO zabezpieczenie
    for row in rows:
        return row
