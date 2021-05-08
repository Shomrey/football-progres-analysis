from Database.getAllValuesHelper import select_player_than_not_have_values_yet
import os
import pandas as pd
from transfermarkt.Scrapper import Scrapper

cwd = os.getcwd()

scrapper = Scrapper()

#done
# players = select_player_than_not_have_values_yet(db_path="..//Database//fpa-database.db")
#
# historic_values = []
# for player in players:
#     player_reference = "https://www.transfermarkt.com" + player[0]
#     print(player_reference)
#     player_values = scrapper.scrap_historical_values(scrapper.get_url_with_historical_values(player_reference))
#     for value in player_values:
#         historic_values.append([player_reference] + value)
#
# df = pd.DataFrame(historic_values, columns=['player_reference','value', 'club', 'date'])
# df.to_csv(os.path.join('', "csv", "Values_Missing.csv"))
#done

# data = pd.read_csv(os.path.join('', "csv", "Values_Missing2.csv"))
# historic_values = []
#
# for index, row in data.iterrows():
#     print(row[1])
#
#
#     player_reference =  row[1]
#     # print("***")
#     print(player_reference)
#     # print("***")
#
#     player_values = scrapper.scrap_historical_values(scrapper.get_url_with_historical_values_v2(player_reference))
#     for value in player_values:
#         historic_values.append([player_reference] + value)
#
# df = pd.DataFrame(historic_values, columns=['player_reference','value', 'club', 'date'])
# df.to_csv(os.path.join('', "csv", "Values_Missing3.csv"))


# data = pd.read_csv(os.path.join('', "csv", "Values_Missing4.csv"))
# historic_values = []
#
# for index, row in data.iterrows():
#     print(row[1])
#
#
#     player_reference =  row[1]
#     # print("***")
#     print(player_reference)
#     # print("***")
#
#     player_values = scrapper.scrap_historical_values(scrapper.get_url_with_historical_values_v2(player_reference))
#     for value in player_values:
#         historic_values.append([player_reference] + value)
#
# df = pd.DataFrame(historic_values, columns=['player_reference','value', 'club', 'date'])
# df.to_csv(os.path.join('', "csv", "Values_Missing5.csv"))

# data = pd.read_csv(os.path.join('', "csv", "Values_Missing6.csv"))
# historic_values = []
#
# for index, row in data.iterrows():
#     print(row[1])
#
#
#     player_reference =  row[1]
#     # print("***")
#     print(player_reference)
#     # print("***")
#
#     player_values = scrapper.scrap_historical_values(scrapper.get_url_with_historical_values_v2(player_reference))
#     for value in player_values:
#         historic_values.append([player_reference] + value)
#
# df = pd.DataFrame(historic_values, columns=['player_reference','value', 'club', 'date'])
# df.to_csv(os.path.join('', "csv", "Values_Missing7.csv"))