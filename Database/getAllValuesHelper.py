import sqlite3


def select_player_than_not_have_values_yet(db_path="fpa-database-fix.db"):
    sqlite_connection = sqlite3.connect(db_path)
    cursor = sqlite_connection.cursor()
    sql_select = '''select url from players_transfermarkt as pt where pt.url not in (select player_url from player_values as pv) group by url'''
    cursor.execute(sql_select)

    rows = cursor.fetchall()

    for row in rows:
        print(row[0])
    sqlite_connection.close()
    return rows
