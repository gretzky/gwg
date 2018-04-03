#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import os
import platform
import sys
import datetime
import requests
from colorama import init, Fore, Style
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_url(url):
    """
    Get the url

    :param url: given url

    :return: page
    """
    response = requests.Session()
    retries = Retry(total=10, backoff_factor=.1)
    response.mount('http://', HTTPAdapter(max_retries=retries))

    try:
        response = response.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        return None

    return response


def get_schedule():
  url = 'https://statsapi.web.nhl.com/api/v1/schedule'

  response = get_url(url)
  time.sleep(1)
  return json.loads(response.text)

schedule = []
schedule_json = get_schedule()

REFRESH_TIME = 30
API_URL = 'https://statsapi.web.nhl.com/api/v1/schedule'
TEST = False

def main():
    while True:
        for day in schedule_json['dates']:
            for game in day['games']:
                game_status = game['status']['detailedState']
                game_type = game['gameType']
                away_team = Style.BRIGHT + game['teams']['away']['team']['name'] + Style.RESET_ALL
                home_team = Style.BRIGHT + game['teams']['home']['team']['name'] + Style.RESET_ALL
                away_score = game['teams']['away']['score']
                home_score = game['teams']['home']['score']

                if game_status == 'Final':
                    if int(away_score) < int(home_score):
                        home_team = Style.BRIGHT + Fore.GREEN + home_team + Style.RESET_ALL
                    elif int(away_score) > int(home_score):
                        away_team = Style.BRIGHT + Fore.GREEN + away_team + Style.RESET_ALL

                def get_status():
                    if game_status == 'In Progress':
                        return Style.BRIGHT + Fore.CYAN + '(' + 'In Progress'.upper() + ')' + Style.RESET_ALL
                    elif game_status == 'Scheduled':
                        return Style.BRIGHT + Fore.YELLOW + '(' + 'Scheduled'.upper() + ')' + Style.RESET_ALL
                    elif game_status == 'Final':
                        return Style.BRIGHT + Fore.MAGENTA + '(' + 'Final'.upper() + ')' + Style.RESET_ALL
                    elif game_status == 'Pre-Game':
                        return Style.BRIGHT + Fore.YELLOW + '(' + 'Pre-Game'.upper() + ')' + Style.RESET_ALL

                header_text = '\n'  + '🏒 🥅 🏒 🥅 🏒 🥅' + '\n' + away_team + ' @ ' + home_team + '\n' + str(away_score) + ' - ' + str(home_score) + '\n' + str(get_status())

                print(header_text)

        if TEST is True:
            sys.exit(0)
        else:
            time.sleep(REFRESH_TIME)
            print('\n')

def parse_arguments(arguments):
    '''process the arguments provided at runtime'''
    for index in range(1, len(arguments)):
        argument = arguments[index]

        if argument == '--test' or argument == '-t':
            print('Running in TEST mode.\n')
            global TEST
            TEST = True

if __name__ == '__main__':
    init()
    parse_arguments(sys.argv)
    main()