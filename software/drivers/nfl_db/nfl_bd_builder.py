from bs4 import BeautifulSoup
import urllib3
import json
import requests
import os
from lxml import etree

"""
url = 'http://www.nfl.com/ajax/scorestrip?season=2017&seasonType=REG&week=12'

    season = 2017
    game_type = 'REG'
    week = 12


tree = etree.parse(url)
root = tree.getroot()
root_child = root.getchildren()

for t in root_child[0]:
    print(t.attrib)
    
# def main():
#     file_path = '/User/Jay/Desktop'
#     file_name = '2017111211_gtd.json'
#     full_path = os.path.join(file_path, file_name)
"""


class NflDatabaseBuilder:

    def get_week_raw_json_data(self, season: int, game_type: str, week: int):
        """

        :param season: the year the nfl games were played
        :param game_type: the game type of the nfl games played. options are PRE, REG or POST
        :param week: the week number the nfl games were played
        :return: None
        """
        # raw_data_directory = os.path.realpath(__file__)

        week_url = 'http://www.nfl.com/ajax/scorestrip?season={year}&seasonType={game_type}&week={week}'.format(
            year=season, game_type=game_type, week=week)
        week_tree = etree.parse(week_url)
        week_root = week_tree.getroot()
        week_root_child = week_root.getchildren()

        # get the individual game codes and save raw json data
        for child in week_root_child[0]:
            game_code = child.attrib['eid']

            # build nlf.com url for raw data and get raw json
            game_data_url = "http://www.nfl.com/liveupdate/game-center/{game_code}/{game_code}_gtd.json".format(
                game_code=game_code)
            game_data_raw_json = requests.get(game_data_url).json()

            # get home team and away team name abbriviations from raw json
            home_team_abbr = game_data_raw_json[game_code]["home"]["abbr"]
            away_team_abbr = game_data_raw_json[game_code]["away"]["abbr"]

            #build file name to save raw json as and save
            file_path = os.path.join(os.path.realpath(__file__), '..', 'raw_json','season_{season}',
                                     'game_type_{game_type}','week_{week}').format(
                season=season, game_type=game_type, week=week)
            file_name = "{date}_{season}_{game_type}_{week}_{home}vs{away}.json".format(
                date=game_code[0:8], season=season, game_type=game_type, week=week, home=home_team_abbr,
                away=away_team_abbr)
            full_path = os.path.join(file_path, file_name)

            # make directory if it doesn't exist
            if not os.path.isdir(file_path):
                os.makedirs(file_path)

            # dump json data
            with open(full_path, 'w') as j:
                json.dump(game_data_raw_json, j)
