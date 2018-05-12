from lxml import etree
import datetime

# url = 'http://www.nfl.com/ajax/scorestrip?season=2017&seasonType=REG&week=12'

tree = etree.parse(url)
root = tree.getroot()
root_child = root.getchildren()

for t in root_child[0]:
    print(t.attrib)


class DataBaseUpdater:
    def __init__(self):



    def get_week_raw_json(year: int, game_type: str, week: int):



        # verify year, game and week are valid
        _verify_game_details(year, game_type, week)

        url = 'http://www.nfl.com/ajax/scorestrip?season={}&seasonType={}&week={}'.format(year, game_type, week)







    def _verify_game_details(year: int, game_type: str, week: int):
        """

        :param year:
        :param game_type:
        :param week:
        :return:
        """
        current_year = datetime.datetime.now().year
        oldest_year = 2009

        if current_year <= year <= oldest_year:
            raise ValueError('The year provided is too old, there is no nfl data for that year')
        if year >= current_year
            raise ValueError('The year provided is in the future, games for this year have not been played yet')


"""
---------------------------------------
not sure what to do with the above code
---------------------------------------
"""
from bs4 import BeautifulSoup
import urllib3
import json
import requests
import os
from lxml import etree

"""
url = 'http://www.nfl.com/ajax/scorestrip?season=2017&seasonType=REG&week=12'

tree = etree.parse(url)
root = tree.getroot()
root_child = root.getchildren()

for t in root_child[0]:
    print(t.attrib)
"""

def main():
    season = 2017
    game_type = 'REG'
    week = 12

    get_week_raw_json_data(season=season, game_type=game_type, week=week)

def get_week_raw_json_data(season: int, game_type: str, week: int):
    """

    :param season: the year the nfl games were played
    :param game_type: the game type of the nfl games played. options are PRE, REG or POST
    :param week: the week number the nfl games were played
    :return: None
    """
    raw_data_directory = os.path.realpath(__file__)

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


# def main():
#     file_path = '/User/Jay/Desktop'
#     file_name = '2017111211_gtd.json'
#     full_path = os.path.join(file_path, file_name)

if __name__ == '__main__':
    main()
