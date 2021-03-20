from transfermarkt.Scrapper import Scrapper

scrapper = Scrapper()
records = scrapper.scrap_historical_values("https://www.transfermarkt.com/brandon-williams/marktwertverlauf/spieler/507700")

#records = scrapper.scrap_historical_values("https://www.transfermarkt.com/gianluigi-buffon/marktwertverlauf/spieler/5023")
print(records)

# records = scrapper.scrap_clubs_in_league()
# print(records)

# records = scrapper.scrap_players_in_team("https://www.transfermarkt.com/fc-liverpool/startseite/verein/31/saison_id/2020")
# print(records)
#
# records = scrapper.combine_club_and_players()
# for record in records:
#     print(records)