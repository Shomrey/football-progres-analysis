from transfermarkt.Scrapper import Scrapper
import pandas as pd

import os

cwd = os.getcwd()

scrapper = Scrapper()

clubs = scrapper.scrap_clubs_in_league()
df = pd.DataFrame(clubs, columns=['club_name', 'reference', 'number_of_footballers', 'total_value'])
if not os.path.isdir('csv'):
    os.mkdir('csv')
df.to_csv(os.path.join('', "csv", "Clubs.csv"))

players = []
for club in clubs:
    club_reference = "https://www.transfermarkt.com" + club[1]
    club_players = scrapper.scrap_players_in_team(club_reference)
    for player in club_players:
        players.append([club_reference] + player)

    # for player in players:
    #     print(player)
df = pd.DataFrame(players, columns=['club_reference','href', 'name_and_surname', 'position', 'market_value', 'date_of_birth', 'country'])
df.to_csv(os.path.join('', "csv", "Players.csv"))




historic_values = []
for player in players:
    player_reference = "https://www.transfermarkt.com" + player[1]
    print(player_reference)
    player_values = scrapper.scrap_historical_values(scrapper.get_url_with_historical_values(player_reference))
    for value in player_values:
        historic_values.append([player_reference] + value)

df = pd.DataFrame(historic_values, columns=['player_reference','value', 'club', 'date'])
df.to_csv(os.path.join('', "csv", "Values.csv"))
