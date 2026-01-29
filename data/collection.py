import requests
import os
import time

import pandas as pd

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def main():
    headers = { 'X-Auth-Token': API_KEY}

    season = input("What season do u want (enter in the year start date so i don't have to code more pls): ")
    url = (f"https://api.football-data.org/v4/competitions/PL/matches?season={season}")
    response = requests.get(url, headers=headers)
    print(response.json())

    dataframe = clean_match_data(response.json()['matches'])
    dataframe.to_csv(f'data/pl_matches_{season}-{int(season) + 1}.csv', index=False)




def clean_match_data(matches):
    cleaned = []

    for match in matches:
        cleaned.append({
            'match_id': match['id'],
            'date': match['utcDate'],
            'matchday': match['matchday'],
            
            # teams
            'home_team_id': match['homeTeam']['id'],
            'home_team': match['homeTeam']['shortName'],
            'away_team_id': match['awayTeam']['id'],
            'away_team': match['awayTeam']['shortName'],
            
            # scores
            'home_goals': match['score']['fullTime']['home'],
            'away_goals': match['score']['fullTime']['away'],
            'home_goals_ht': match['score']['halfTime']['home'],
            'away_goals_ht': match['score']['halfTime']['away'],
            
            # Result 
            'result': match['score']['winner'] 
        })
    
    df = pd.DataFrame(cleaned)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    return df


if __name__ == "__main__":
    main()


    