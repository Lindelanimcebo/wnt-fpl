import requests
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint

league_id = '<some_value>' # TODO: This should be an argument passed in from a Secret
base_url = 'https://fantasy.premierleague.com/api'

def get_league_standings(league_id):
    url = f"{base_url}/leagues-classic/{league_id}/standings/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve data from FPL API with status code {response.status_code}")


def get_manager_standings(league_data):
    standings = league_data['standings']['results']
    manager_data = []

    for manager in standings:
        entry_id = manager['entry']
        player_name = manager['player_name']
        entry_name = manager['entry_name']

        # Fetch gameweek history for this manager
        manager_history_url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/history/"
        history_data = requests.get(manager_history_url).json()

        # Extract total points for each gameweek
        gameweek_points = [gw['total_points'] for gw in history_data['current']]

        # Do cumulative points
        gameweek_standings = [gw['standing'] for gw in history_data['current']]

        manager_data.append({
            'entry_name': entry_name,
            'player_name': player_name,
            'gameweek_points': gameweek_points,
            'gameweek_standings': gameweek_standings
        })

    return pd.DataFrame(manager_data)

def plot_points_over_time(df):
    plt.figure(figsize=(20, 12))

    for i, row in df.iterrows():
        gameweeks = range(1, len(row['gameweek_points']) + 1)
        plt.plot(range(1, len(row['gameweek_points']) + 1), row['gameweek_points'], label=row['entry_name'])
        plt.text(gameweeks[-1] + 0.1, row['gameweek_points'][-1],f"{row['entry_name']}({row['gameweek_points'][-1]})",
                 verticalalignment='center')

    plt.title('We Need Therapy - Points Over Time')
    plt.xlabel('Gameweek')
    plt.ylabel('Points')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    league_data = get_league_standings(league_id)
    manager_data = get_manager_standings(league_data)
    pprint(manager_data)
    plot_points_over_time(manager_data)
