from transfermarkt.Scrapper import Scrapper
import pandas as pd

import os

cwd = os.getcwd()

scrapper = Scrapper()

seasons = ['2015', '2016', '2017', '2018', '2019', '2020']
for season in seasons:
    league_url = "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/saison_id/" + season
    clubs = scrapper.scrap_clubs_in_league(league_url=league_url)
    df = pd.DataFrame(clubs, columns=['club_name', 'reference', 'number_of_footballers', 'total_value'])
    if not os.path.isdir('csv'):
        os.mkdir('csv')
    df.to_csv(os.path.join('', "csv", "Clubs_" + season + ".csv"))

    players = []
    for club in clubs:
        club_reference = "https://www.transfermarkt.com" + club[1]
        club_players = scrapper.scrap_players_in_team(club_reference)
        for player in club_players:
            players.append([club_reference] + player)

        # for player in players:
        #     print(player)
    df = pd.DataFrame(players, columns=['club_reference', 'href', 'name_and_surname', 'position', 'market_value',
                                        'date_of_birth', 'country'])
    df.to_csv(os.path.join('', "csv", "Players_" + season + ".csv"))



