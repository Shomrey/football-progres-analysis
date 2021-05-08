import os
from decimal import Decimal
import pandas as pd
from datetime import datetime


class CsvTransformers:

    def __init__(self):
        pass

    def get_string_monetary_value_as_decimal(self, string_value2=None):
        string_value = string_value2.strip('€')
        string_number = ""
        factor = ""
        not_end_of_number = True
        for character in string_value:
            if not_end_of_number and (character.isdigit() or character == '.'):
                string_number = string_number + character
            else:
                not_end_of_number = False
                factor = factor + character

        number_factor = 1
        if factor[-1] != ' ':
            factor = factor + ' '
        if factor.startswith("Th."):
            number_factor = 1000
        if factor.startswith("m"):
            number_factor = 1000000
        if factor.startswith("bn"):
            number_factor = 1000000000
        if string_number != "":
            euros_decimal = Decimal(string_number) * number_factor
        else:
            euros_decimal = Decimal(-1)
        # print(string_value + "|" +string_number + "|" +factor +"|"+ str(number_factor) + "|"+ str(euros_decimal) )
        # jeśli nie ma ceny to przyjmujemy cenę równą -1 na danych wejściowych
        return euros_decimal

    def transform_clubs(self, file_name="Clubs.csv"):
        # csvTransformers = CsvTransformers()
        # euros_decimal = csvTransformers.get_string_monetary_value_as_decimal("€1.03bn")
        # print(euros_decimal)

        filename = os.path.join("csv", file_name)
        df = pd.read_csv(filename)
        for i, row in df.iterrows():
            df.at[i, 'total_value'] = self.get_string_monetary_value_as_decimal(df.at[i, 'total_value'])
        df.drop('Unnamed: 0', axis=1, inplace=True)
        filename = os.path.join("csv_transform", file_name)
        df.to_csv(filename, index=False)

    def get_player_birthdate(self, string_value):
        string_value = string_value.split(' (')
        date_time_obj = datetime.strptime(string_value[0], '%b %d, %Y')
        return date_time_obj

    def get_date_time(self, string_value):
        date_time_obj = None
        try:
            date_time_obj = datetime.strptime(string_value, '%b %d, %Y')
        except Exception:
            print(string_value)
        return date_time_obj

    def transform_players(self, file_name="Players.csv"):
        filename = os.path.join("csv", file_name)
        df = pd.read_csv(filename)
        for i, row in df.iterrows():
            df.at[i, 'date_of_birth'] = self.get_player_birthdate(df.at[i, 'date_of_birth'])
            df.at[i, 'market_value'] = self.get_string_monetary_value_as_decimal(df.at[i, 'market_value'])
        df.drop('Unnamed: 0', axis=1, inplace=True)
        filename = os.path.join("csv_transform", file_name)
        df.to_csv(filename, index=False)

    def transform_values(self):
        print("sfdsdf")
        filename = os.path.join("csv", "Values.csv")
        df = pd.read_csv(filename)
        print(df)
        for i, row in df.iterrows():
            df.at[i, 'date'] = self.get_date_time(df.at[i, 'date'])
        df.drop('Unnamed: 0', axis=1, inplace=True)
        filename = os.path.join("csv_transform", "Values.csv")
        df.to_csv(filename, index=False)


helper = CsvTransformers()

seasons = ['2015', '2016', '2017', '2018', '2019', '2020']

for season in seasons:
    helper.transform_clubs("Clubs_" + season + ".csv")
    helper.transform_players("Players_" + season + ".csv")

# helper.transform_players()
# helper.transform_values()


# euros = helper.get_string_monetary_value_as_decimal("€56.00m")
# print(euros)
