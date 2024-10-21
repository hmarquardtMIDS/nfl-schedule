NFL_TEAMS = {
    "AFC": {
        "East": [
            "Buffalo Bills",
            "Miami Dolphins",
            "New England Patriots",
            "New York Jets"
        ],
        "North": [
            "Baltimore Ravens",
            "Cincinnati Bengals",
            "Cleveland Browns",
            "Pittsburgh Steelers"
        ],
        "South": [
            "Houston Texans",
            "Indianapolis Colts",
            "Jacksonville Jaguars",
            "Tennessee Titans"
        ],
        "West": [
            "Denver Broncos",
            "Kansas City Chiefs",
            "Las Vegas Raiders",
            "Los Angeles Chargers"
        ]
    },
    "NFC": {
        "East": [
            "Dallas Cowboys",
            "New York Giants",
            "Philadelphia Eagles",
            "Washington Commanders"
        ],
        "North": [
            "Chicago Bears",
            "Detroit Lions",
            "Green Bay Packers",
            "Minnesota Vikings"
        ],
        "South": [
            "Atlanta Falcons",
            "Carolina Panthers",
            "New Orleans Saints",
            "Tampa Bay Buccaneers"
        ],
        "West": [
            "Arizona Cardinals",
            "Los Angeles Rams",
            "San Francisco 49ers",
            "Seattle Seahawks"
        ]
    }
}

def get_all_teams():
    """
    Returns a flat list of all NFL teams.
    """
    return [team for conference in NFL_TEAMS.values() for division in conference.values() for team in division]

def get_team_info(team_name):
    """
    Returns the conference and division for a given team name.
    """
    for conference, divisions in NFL_TEAMS.items():
        for division, teams in divisions.items():
            if team_name in teams:
                return conference, division
    return None, None
