import os

import pandas as pd


def get_data_frame_from_csv(file_name):
    filename = os.path.join("csv_transfermarkt", file_name)
    return pd.read_csv(filename)


df = get_data_frame_from_csv("Clubs.csv")

print(df)


for index, row in df.iterrows():
       print(row['club_name'])
