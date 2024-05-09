from api_functions import fetch_recent_matches, fetch_team_info, fetch_league_standings, fetch_team_id, fetch_match_fixtures
from datetime import datetime
import requests
def print_team_info_and_standings(team_name):
    team_id = fetch_team_id(team_name)
    if team_id:
        team_info = fetch_team_info(team_id)
        league_id = team_info.get("activeCompetitions")[0].get("id")
        if league_id:
            print(f"Team Information - {team_name}:")
            print(f"Name: {team_info.get('name', 'N/A')}")
            print(f"Venue: {team_info.get('venue', 'N/A')}")
            print(f"League: {team_info.get('league', {}).get('name', 'N/A')}")
            print("\nLeague Standings:")
            league_standings = fetch_league_standings(league_id)
            print(league_standings)
            standings = league_standings.get("standings")[0]["table"]
            if standings:
                for standing in standings:
                    team_name = standing["teamName"]
                    position = standing["position"]
                    played_games = standing["playedGames"]
                    points = standing["points"]
                    print(f"{team_name} - Position: {position}, Played: {played_games}, Points: {points}")
            else:
                print("League table is empty")
        else:
            print(f"No league information found for {team_name}.")
    else:
        print(f"Team '{team_name}' not found.")



def generate_search_snippets(query, fixtures):
    query_tokens = query.lower().split()
    snippets = []
    for fixture in fixtures['matches']:
        home_team = fixture["homeTeam"]["name"].lower().split()[0]
        away_team = fixture["awayTeam"]["name"].lower().split()[0]
        date = datetime.strptime(fixture["utcDate"], "%Y-%m-%dT%H:%M:%S%z").strftime("%d %b %Y")
        if home_team in query_tokens and away_team in query_tokens:
            snippet = f"{home_team} vs {away_team} on {date}"
            snippets.append(snippet)
    return snippets

query = "Arsenal Everton upcoming match"
matchday = 38  
fixtures = fetch_match_fixtures(matchday)

snippets = generate_search_snippets(query, fixtures)

if snippets:
    print("Search results:")
    for snippet in snippets:
        print(snippet)
else:
    print("No relevant information found.")

team_id = fetch_team_id("everton")
print_team_info_and_standings("everton")

recent_matches = fetch_recent_matches(fetch_team_id("everton"))
if recent_matches:
    for match in recent_matches:
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        score = f"{match['score']['fullTime']['homeTeam']} - {match['score']['fullTime']['awayTeam']}"
        date = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%S%z").strftime("%d %b %Y")
        print(f"{home_team} {score} {away_team} on {date}")
else:
    print(f"No recent matches found for team ID {team_id}.")