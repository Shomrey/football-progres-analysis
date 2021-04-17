from transfermarkt.Scrapper import Scrapper
import pandas as pd
import os

scrapper = Scrapper()


# extra_srapping_values_urls =[
# "https://www.transfermarkt.com/kevin-de-bruyne/profil/spieler/88755",
# "https://www.transfermarkt.com/trent-alexander-arnold/profil/spieler/314353",
# "https://www.transfermarkt.com/neco-williams/profil/spieler/503680",
# "https://www.transfermarkt.com/mohamed-salah/profil/spieler/148455",
# "https://www.transfermarkt.com/victor-lindelof/profil/spieler/184573",
# "https://www.transfermarkt.com/hannibal-mejbri/profil/spieler/607224",
# "https://www.transfermarkt.com/pierre-emile-hojbjerg/profil/spieler/167799",
# "https://www.transfermarkt.com/lucas-moura/profil/spieler/77100",
# "https://www.transfermarkt.com/eldin-jakupovic/profil/spieler/2857",
# "https://www.transfermarkt.com/abdoulaye-doucoure/profil/spieler/127187",
# "https://www.transfermarkt.com/vitinha/profil/spieler/487469",
# "https://www.transfermarkt.com/tom-heaton/profil/spieler/34130",
# "https://www.transfermarkt.com/john-mcginn/profil/spieler/193116",
# "https://www.transfermarkt.com/jacob-ramsey/profil/spieler/503749",
# "https://www.transfermarkt.com/paul-dummett/profil/spieler/170321",
# "https://www.transfermarkt.com/javier-manquillo/profil/spieler/162029",
# "https://www.transfermarkt.com/dwight-gayle/profil/spieler/196522",
# "https://www.transfermarkt.com/dan-nlundulu/profil/spieler/346482",
# "https://www.transfermarkt.com/jose-izquierdo/profil/spieler/147094",
# "https://www.transfermarkt.com/ezgjan-alioski/profil/spieler/129604",
# "https://www.transfermarkt.com/jack-harrison/profil/spieler/417346",
# "https://www.transfermarkt.com/mamadou-sakho/profil/spieler/47713",
# "https://www.transfermarkt.com/connor-wickham/profil/spieler/95435",
# "https://www.transfermarkt.com/phil-jagielka/profil/spieler/13520",
# "https://www.transfermarkt.com/john-fleck/profil/spieler/54383",
# "https://www.transfermarkt.com/oliver-burke/profil/spieler/341317",
# "https://www.transfermarkt.com/darnell-furlong/profil/spieler/351755"
# ]

extra_srapping_values_urls =[
"https://www.transfermarkt.com/hannibal-mejbri/profil/spieler/607224",
"https://www.transfermarkt.com/john-mcginn/profil/spieler/193116",
"https://www.transfermarkt.com/dwight-gayle/profil/spieler/196522",
"https://www.transfermarkt.com/mamadou-sakho/profil/spieler/47713"
]

historic_values = []
for url in extra_srapping_values_urls:
    player_values = scrapper.scrap_historical_values(scrapper.get_url_with_historical_values(url))
    for value in player_values:
        historic_values.append([url] + value)

df = pd.DataFrame(historic_values, columns=['player_reference','value', 'club', 'date'])
df.to_csv(os.path.join('', "csv", "Values_extra_time2.csv"))