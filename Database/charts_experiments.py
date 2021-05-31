import sqlite3

import matplotlib.dates as mdates
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

import numpy as np


def get_values_from_db(transfermarkt_player_id):
    cnx = sqlite3.connect('fpa-database-fix.db')

    cur = cnx.cursor()
    cur.execute(
        """select date_stamp, player_value, player_club from player_values_transfermarkt where transfermarkt_player_id = ? order by date_stamp""",
        (transfermarkt_player_id,))

    rows = cur.fetchall()

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

    plt.show()
    if (cnx): cnx.close()


def get_fpl_first_name_and_last_name_from_transfermarkt_id(transfermarkt_id):
    sqlite_connection = sqlite3.connect("fpa-database-fix.db")
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


def head_to_head_comparison(transfermarkt_player_id_1, transfermarkt_player_id_2):
    cnx = sqlite3.connect('fpa-database-fix.db')

    cur = cnx.cursor()
    cur.execute(
        """select date_stamp, player_value, player_club from player_values_transfermarkt where transfermarkt_player_id = ? order by date_stamp""",
        (transfermarkt_player_id_1,))

    rows_1 = cur.fetchall()

    cur.execute(
        """select date_stamp, player_value, player_club from player_values_transfermarkt where transfermarkt_player_id = ? order by date_stamp""",
        (transfermarkt_player_id_2,))
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
    first_tuple = get_fpl_first_name_and_last_name_from_transfermarkt_id(transfermarkt_player_id_1)
    second_tuple = get_fpl_first_name_and_last_name_from_transfermarkt_id(transfermarkt_player_id_2)
    axes.legend([first, second], [first_tuple[0] + ' ' + first_tuple[1], second_tuple[0] + ' ' + second_tuple[1]],
                loc='lower center')
    # Manually add the first legend back
    axes.add_artist(legend1)

    plt.show()
    if (cnx): cnx.close()


get_values_from_db(1)
get_values_from_db(6)
get_values_from_db(1788)

head_to_head_comparison(1, 6)
head_to_head_comparison(488, 1788)
