from unidecode import unidecode


text = "Björn, Łukasz and Σωκράτης."

print(unidecode(text))

import sqlite3
import pandas as pd
# Create your connection.
cnx = sqlite3.connect('fpa-database.db')

df_transfer = pd.read_sql_query("SELECT * FROM players_transfermarkt", cnx)
print(df_transfer)

df_fpl = pd.read_sql_query("SELECT * FROM players", cnx)

counter = 0
for index_transfer, row_transfer in df_transfer.iterrows():
    for index_fpl, row_fpl in df_fpl.iterrows():
        if unidecode(row_transfer["player_name"]) ==  unidecode(row_fpl["first_name"] + " " +row_fpl["second_name"]):
            print("******")
            print(row_transfer)
            print(counter)
            counter = counter+1

    # print(row["c1"], row["c2"])
