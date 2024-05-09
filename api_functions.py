import requests
from datetime import datetime

api_key = ""
base_api_url = "https://api.football-data.org/v2/"
headers = {"X-Auth-Token": api_key}

def fetch_match_fixtures(matchday):
    api_url = "https://api.football-data.org/v2/competitions/PL/matches"
    params = {
        "matchday": matchday,
        "status": "SCHEDULED"
    }
    response = requests.get(api_url, headers=headers, params=params)
    return response.json()

def fetch_recent_matches(team_id):
    api_url = f"{base_api_url}teams/{team_id}/matches"
    params = {"status": "FINISHED"}
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        matches = response.json().get("matches", [])
        return matches[:5]
    except requests.RequestException as e:
        print(f"Error fetching recent matches for team ID {team_id}: {e}")
        return []

def fetch_team_info(team_id):
    api_url = f"{base_api_url}teams/{team_id}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching team info for team ID {team_id}: {e}")
        return None

def fetch_league_standings(league_id):
    api_url = f"{base_api_url}competitions/{league_id}/standings"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching league standings for league ID {league_id}: {e}")
        return None

def fetch_team_id(team_name):
    params = {"name": team_name}
    try:
        response = requests.get(f"{base_api_url}teams", headers=headers, params=params)
        response.raise_for_status()
        teams = response.json().get("teams", [])
        if teams:
            for team in teams:
                if team_name.lower() in team["name"].lower():
                    return team["id"]
        print(f"Team '{team_name}' not found.")
        return None
    except requests.RequestException as e:
        print(f"Error fetching team ID: {e}")
        return None