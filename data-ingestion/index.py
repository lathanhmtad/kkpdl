import requests
import pandas as pd
from collections import defaultdict
import time
import json
import random
import line_ups as lus
import time
from datetime import datetime, timedelta

DATABASE_API = 'http://localhost:5000/db-api'

API_URL = 'https://api-football-v1.p.rapidapi.com/v3'
HEADERS = {
    'x-rapidapi-key': '9311b9ba16msh3e8ac06e4d4605fp194a07jsne4c30661ccba',
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
}

LEAGUE_ID = 39 # Premier league
SEASON = 2024 # Current season

def fetch_team_recent_matches(t_id, num_matches=10, form_date = None, to_date = None):
    print(f"Fetching matches for team id {t_id}...")

    results = []

    fixtures = requests.get(f'{API_URL}/fixtures', headers=HEADERS, params={'team': t_id, 'last': num_matches, 'league': LEAGUE_ID, 'from': form_date, 'to': to_date}).json().get('response', [])
    
    for fixture in fixtures:
        team_id = t_id
        fixture_id = fixture['fixture']['id']
        match_date = fixture['fixture']['date']
        team_name = fixture['teams']['home']['name'] if fixture['teams']['home']['id'] == t_id else fixture['teams']['away']['name']
        away_team_id = fixture['teams']['away']['id'] if fixture['teams']['away']['id'] != t_id else fixture['teams']['home']['id']
        away_team_name = fixture['teams']['away']['name'] if fixture['teams']['away']['id'] != t_id else fixture['teams']['home']['name']
        goals_home = fixture['goals']['away'] if t_id == fixture['teams']['away']['id'] else fixture['goals']['home']
        goals_away = fixture['goals']['away'] if t_id != fixture['teams']['away']['id'] else fixture['goals']['home']
        
        yellow_cards_home = 0
        yellow_cards_away = 0
        red_cards_home = 0
        red_cards_away = 0
        corner_home = 0
        corner_away = 0
        statistics = requests.get(f'{API_URL}/fixtures/statistics', headers=HEADERS, params={'fixture': fixture_id}).json().get('response', [])
        for event in statistics:
            if event['team']['id'] == t_id:
                for statistic in event['statistics']:
                    if statistic['type'] == 'Yellow Cards':
                        yellow_cards_home = statistic['value'] or 0
                    if statistic['type'] == 'Red Cards':
                        red_cards_home = statistic['value'] or 0
                    if statistic['type'] == 'Corner Kicks':
                        corner_home = statistic['value'] or 0
            else:
                for statistic in event['statistics']:
                    if statistic['type'] == 'Yellow Cards':
                        yellow_cards_away = statistic['value'] or 0
                    if statistic['type'] == 'Red Cards':
                        red_cards_away = statistic['value'] or 0
                    if statistic['type'] == 'Corner Kicks':
                        corner_away = statistic['value'] or 0
        team_strength_home = 100
        team_strength_away = 100
        line_ups = requests.get(f'{API_URL}/fixtures/lineups', headers=HEADERS, params={'fixture': fixture_id}).json().get('response', [])
        for line_up in line_ups:
            if line_up['team']['id'] == t_id:
                for lu in lus.team_line_ups:
                    if lu['team_id'] == t_id:
                        startXI = line_up['startXI']
                        best_line_up = lu['best_line_up']
                        for player in startXI:
                            if player['player']['name'] not in best_line_up:
                                team_strength_home -= 9.09
            else:
                for lu in lus.team_line_ups:
                    if lu['team_id'] == line_up['team']['id']:
                        startXI = line_up['startXI']
                        best_line_up = lu['best_line_up']
                        for player in startXI:
                            if player['player']['name'] not in best_line_up:
                                team_strength_away -= 9.09 

        match_result = None
        if goals_home == goals_away:
            match_result = 'DRAW'
        elif goals_home > goals_away:
            match_result = 'WIN'
        else:
            match_result = 'LOSE'

        results.append({
            'team_id': t_id,
            'fixture_id': fixture_id,
            'match_date': match_date,
            'team_name': team_name,
            'away_team_id': away_team_id,
            'away_team_name': away_team_name,
            'goals_home': goals_home,
            'goals_away': goals_away,
            'yellow_cards_home': yellow_cards_home,
            'yellow_cards_away': yellow_cards_away,
            'red_cards_home': red_cards_home,
            'red_cards_away': red_cards_away,
            'corner_home': corner_home,
            'corner_away': corner_away,
            'team_strength_home': team_strength_home,
            'team_strength_away': team_strength_away,
            'match_result': match_result
        })

    return results

def call_api_interval_5_phut():
    results = []

    fixtures = requests.get(f'{API_URL}/fixtures', headers=HEADERS, params={'team': t_id, 'last': num_matches, 'league': LEAGUE_ID, 'from': form_date, 'to': to_date}).json().get('response', [])
    
    for fixture in fixtures:
        team_id = t_id
        fixture_id = fixture['fixture']['id']

        check = requests.get(f'{DATABASE_API}/check-fixture-id/{fixture_id}').json().get('exists')
        if(check == 'True' or check == True):
            return

        match_date = fixture['fixture']['date']
        team_name = fixture['teams']['home']['name'] if fixture['teams']['home']['id'] == t_id else fixture['teams']['away']['name']
        away_team_id = fixture['teams']['away']['id'] if fixture['teams']['away']['id'] != t_id else fixture['teams']['home']['id']
        away_team_name = fixture['teams']['away']['name'] if fixture['teams']['away']['id'] != t_id else fixture['teams']['home']['name']
        goals_home = fixture['goals']['away'] if t_id == fixture['teams']['away']['id'] else fixture['goals']['home']
        goals_away = fixture['goals']['away'] if t_id != fixture['teams']['away']['id'] else fixture['goals']['home']
        
        yellow_cards_home = 0
        yellow_cards_away = 0
        red_cards_home = 0
        red_cards_away = 0
        corner_home = 0
        corner_away = 0
        statistics = requests.get(f'{API_URL}/fixtures/statistics', headers=HEADERS, params={'fixture': fixture_id}).json().get('response', [])
        for event in statistics:
            if event['team']['id'] == t_id:
                for statistic in event['statistics']:
                    if statistic['type'] == 'Yellow Cards':
                        yellow_cards_home = statistic['value'] or 0
                    if statistic['type'] == 'Red Cards':
                        red_cards_home = statistic['value'] or 0
                    if statistic['type'] == 'Corner Kicks':
                        corner_home = statistic['value'] or 0
            else:
                for statistic in event['statistics']:
                    if statistic['type'] == 'Yellow Cards':
                        yellow_cards_away = statistic['value'] or 0
                    if statistic['type'] == 'Red Cards':
                        red_cards_away = statistic['value'] or 0
                    if statistic['type'] == 'Corner Kicks':
                        corner_away = statistic['value'] or 0
        team_strength_home = 100
        team_strength_away = 100
        line_ups = requests.get(f'{API_URL}/fixtures/lineups', headers=HEADERS, params={'fixture': fixture_id}).json().get('response', [])
        for line_up in line_ups:
            if line_up['team']['id'] == t_id:
                for lu in lus.team_line_ups:
                    if lu['team_id'] == t_id:
                        startXI = line_up['startXI']
                        best_line_up = lu['best_line_up']
                        for player in startXI:
                            if player['player']['name'] not in best_line_up:
                                team_strength_home -= 9.09
            else:
                for lu in lus.team_line_ups:
                    if lu['team_id'] == line_up['team']['id']:
                        startXI = line_up['startXI']
                        best_line_up = lu['best_line_up']
                        for player in startXI:
                            if player['player']['name'] not in best_line_up:
                                team_strength_away -= 9.09 

        match_result = None
        if goals_home == goals_away:
            match_result = 'DRAW'
        elif goals_home > goals_away:
            match_result = 'WIN'
        else:
            match_result = 'LOSE'

        results.append({
            'team_id': t_id,
            'fixture_id': fixture_id,
            'match_date': match_date,
            'team_name': team_name,
            'away_team_id': away_team_id,
            'away_team_name': away_team_name,
            'goals_home': goals_home,
            'goals_away': goals_away,
            'yellow_cards_home': yellow_cards_home,
            'yellow_cards_away': yellow_cards_away,
            'red_cards_home': red_cards_home,
            'red_cards_away': red_cards_away,
            'corner_home': corner_home,
            'corner_away': corner_away,
            'team_strength_home': team_strength_home,
            'team_strength_away': team_strength_away,
            'match_result': match_result
        })

    return results


def main():
    
    print(check)

    while True:
        # Lấy danh sách các đội từ database
        teams = requests.get(f'{DATABASE_API}/teams').json().get('data', [])
        
        for team in teams:
            recent_matches = call_api_interval_5_phut(
                t_id=team['team_id'],
                num_matches=1,
            )
            
            # Gửi kết quả lên database
            response = requests.post(f'{DATABASE_API}/team-history', json=recent_matches, headers={
                'Content-Type': 'application/json'
            })
        time.sleep(300)

if __name__ == '__main__':
    main()
