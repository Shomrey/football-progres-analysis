import pandas as pd
from unidecode import unidecode
#import unicodedata
#def unidecode(s):
#   return ''.join(c for c in unicodedata.normalize('NFD', s)
#                  if unicodedata.category(c) != 'Mn')

def create_players_guids(player_ids_paths_list):
    names = []
    for path in player_ids_paths_list:
        players = pd.read_csv(path)
        for index, row in players.iterrows():
            names.append(unidecode(row['first_name'])+'|'+unidecode(row['second_name']))
    names = list(dict.fromkeys(names))
    data = [[name.split('|')[0], name.split('|')[1], index] for index, name in enumerate(names)]


    result_df = pd.DataFrame(data, columns=['first_name', 'second_name', 'guid'])
    result_df.to_csv('players_guid.csv', index=False)

#create_players_guids(['player_idlist_16_17.csv','player_idlist_17_18.csv','player_idlist_18_19.csv','player_idlist_19_20.csv','player_idlist_20_21.csv'])

def create_players_data_cleaned(paths_list, years):
    players_guids_df = pd.read_csv('players_guid.csv')
    guids_dict = {}
    players_final_df_list = []
    for index, row in players_guids_df.iterrows():
        guids_dict[row['first_name'] + '|' + row['second_name']] = row['guid']
    for path, year in zip(paths_list, years):
        players_df = pd.read_csv(path)
        year_column = [year] * len(players_df.index)
        guid_column = []
        for index, row in players_df.iterrows():
            name_key = unidecode(row['first_name']) + '|' + unidecode(row['second_name'])
            if name_key in guids_dict:
                guid_column.append(guids_dict[name_key])
            else:
                print(name_key)
                guid_column.append(int(input()))
        players_df.insert(0, 'guid', guid_column)
        players_df['year'] = year_column
        players_final_df_list.append(players_df)
        print('next file')
    players_final_df = pd.concat(players_final_df_list)
    players_final_df.to_csv('players_cleaned.csv', index=False)

#create_players_data_cleaned(['cleaned_players_16_17_test.csv','cleaned_players_17_18.csv','cleaned_players_18_19.csv','cleaned_players_19_20.csv','cleaned_players_20_21.csv'],[2016,2017,2018,2019,2020])
def normalize_names(list_of_paths):
    for path in list_of_paths:
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            row['first_name'] = unidecode(row['first_name'])
            row['second_name'] = unidecode(row['second_name'])
        df.to_csv('unified_players.csv.csv', index=False)

normalize_names(['players_cleaned.csv'])