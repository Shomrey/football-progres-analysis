import re

import requests
from bs4 import BeautifulSoup
import json


class Scrapper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        }

    def combine_club_and_players(self):
        clubs = self.scrap_clubs_in_league()
        complex_records = []
        for club in clubs:
            players = self.scrap_players_in_team("https://www.transfermarkt.com" + club[1])

            for player in players:
                record = [club[0], club[1], player]
                # complex_records.append(record)
        return complex_records

    def scrap_historical_values(self, url):
        records_to_return = []
        try:

            req = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            pretty = soup.prettify()

            text = soup.find_all('script')
            text = str(text[-1])
            text = text.split("'data':", 1)[1]
            text = text.split("}],'credits'", 1)[0]
            text = text.replace('\'', '"')
            text = re.sub(r"\\[x|u][\d|\w][\d|\w]", " ", text)

            tuples = json.loads(text)

            for record in tuples:
                records_to_return.append([record['y'], record['verein'], record['datum_mw']])

        except IndexError:
            records_to_return.append(["-1", "", ""])
        return records_to_return

    def scrap_clubs_in_league(self,
                              league_url="https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/saison_id/2020"):
        req = requests.get(league_url, headers=self.headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        pretty = soup.prettify()

        text = soup.find_all('div', id="main")
        text = text[0].find_all('div', id="wettbewerbsstartseite")
        text = text[0].find_all('div', class_="large-8 columns")
        text = text[0].find_all('div', class_="box")
        text = text[1].find_all('div', class_="responsive-table")
        text = text[0].find_all('div', id="yw1")
        text = text[0].find_all('table', class_="items")
        text = text[0].find_all('tbody')
        text = text[0].find_all('tr')

        records_to_return = []
        for club in text:
            # print(club)
            club = club.find_all('td')
            club0 = club[0]
            str_club = str(club0)

            club_name = str_club.split("img alt=\"", 1)[1]
            club_name = club_name.split("\"", 1)[0]
            # print(club_name)

            href = str(club0)
            href = href.split("href=\"", 1)[1]
            href = href.split("\"", 1)[0]

            footballers_number = club[3].find_all('a')
            footballers_number = str(footballers_number[0]).split(">", 1)[1].split("<", 1)[0]

            summary_value = club[6].find_all('a')
            summary_value = str(summary_value[0]).split(">", 1)[1].split("<", 1)[0]

            records_to_return.append([club_name, href, footballers_number, summary_value])

        return records_to_return

    def scrap_players_in_team(self, url):
        req = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        pretty = soup.prettify()

        text = soup.find_all('div', id="main")
        text = text[0].find_all('div', class_="row vereinsstartseite")
        text = text[0].find_all('div', class_="large-8 columns")
        text = text[0].find_all('div', class_="box kader-widget viewport-tracking")
        text = text[0].find_all('div', class_="responsive-table")
        text = text[0].find_all('div', id="yw1")
        text = text[0].find_all('table', class_="items")
        text = text[0].find_all('tbody')
        text = text[0].find_all('tr')
        # text = text[0].find_all('td')
        records_to_return = []
        iter = 0
        for player in text:
            if (iter % 3 == 0):
                player = player.find_all('td')
                href = str(player[3])
                href = href.split("href=\"", 1)[1]
                href = href.split("\"", 1)[0]
                name_and_surname = (str(player[5]).split(">", 1)[1].split("<", 1)[0])
                position = (str(player[4]).split(">", 1)[1].split("<", 1)[0])
                date_of_birth = (str(player[6]).split(">", 1)[1].split("<", 1)[0])
                country = (str(player[7]).split("img alt=\"", 1)[1].split("\"", 1)[0])
                market_value = (str(player[8]).split(">", 1)[1].split("<", 1)[0])
                # todo second country - sometimes this happens
                records_to_return.append([href, name_and_surname, position, market_value, date_of_birth, country])

            iter += 1

        return records_to_return

    def get_url_with_historical_values(self, player_url):
        first_part = player_url.split("/profil", 1)[0]
        last_part = player_url.split("/profil/", 1)[1]
        return first_part + "/marktwertverlauf/" + last_part
