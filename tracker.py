import json
import requests
from datetime import datetime

def fetch_and_calculate_3rd_place():
    # Fetching live standings from a free Open Data CDN endpoint
    url = "https://www.thestatsapi.com/world-cup/data/standings.json"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}. Falling back to sample structural data.")
        return

    third_placed_teams = []

    # Iterate through all 12 groups (Groups A through L)
    for group in data.get("groups", []):
        group_letter = group.get("letter", "?")
        teams = group.get("teams", [])
        
        # Sort group teams by standard criteria to find the real 3rd place team safely
        teams.sort(key=lambda x: (x.get("points", 0), x.get("goalDifference", 0), x.get("goalsFor", 0)), reverse=True)
        
        if len(teams) >= 3:
            third_team = teams[2]  # Index 2 is the 3rd placed team
            third_placed_teams.append({
                "name": third_team.get("name"),
                "group": group_letter,
                "played": third_team.get("played", 0),
                "points": third_team.get("points", 0),
                "gd": third_team.get("goalDifference", 0),
                "gf": third_team.get("goalsFor", 0),
                "fairPlay": third_team.get("fairPlayPoints", 0)  # Standard fallback
            })

    # Apply FIFA's tiebreaker sorting logic across all 3rd-placed teams
    # Sorting sequence: 1. Points -> 2. Goal Difference -> 3. Goals For -> 4. Fair Play
    third_placed_teams.sort(key=lambda x: (x["points"], x["gd"], x["gf"], x["fairPlay"]), reverse=True)

    # Wrap the output list with a timestamp metadata property
    output_data = {
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "teams": third_placed_teams
    }

    # Save to a dynamic JSON asset file that our HTML dashboard can read
    with open("standings.json", "w") as f:
        json.dump(output_data, f, indent=4)
    print("Successfully generated standings.json file!")

if __name__ == "__main__":
    fetch_and_calculate_3rd_place()
