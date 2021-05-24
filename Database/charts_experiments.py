import sqlite3

import matplotlib.dates as mdates
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

import numpy as np


def get_values_from_db(transfermarkt_player_id):
    cnx = sqlite3.connect('fpa-database.db')

    cur = cnx.cursor()
    cur.execute(
        """select date_stamp, player_value, player_club from player_values_transfermarkt where transfermarkt_player_id = ? order by date_stamp""",
        (transfermarkt_player_id,))

    rows = cur.fetchall()

    print(rows[0])
    print(rows)

    origin = []
    b = []
    clubs = []
    for row in rows:
        origin.append(row[0])
        b.append(row[1]/10**6)
        clubs.append(row[2])

    labels, index = np.unique(clubs, return_inverse=True)


    a = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in origin]

    x = matplotlib.dates.date2num(a)
    formatter = matplotlib.dates.DateFormatter('%Y-%m')

    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)

    axes.xaxis.set_major_formatter(formatter)
    plt.setp(axes.get_xticklabels(), rotation=45)

    sc = axes.scatter(x, b, c = index)
    axes.legend(sc.legend_elements()[0], labels)
    plt.ylabel("Market value [mln euro]")
    plt.plot(x, b, linestyle='dashed')

    plt.show()
    if (cnx): cnx.close()


get_values_from_db(1)
get_values_from_db(6)

