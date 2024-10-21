import json
import os

TOTAL_WEEKS = 18

class Game:
    def __init__(self, home_team, away_team, week):
        self.home_team = home_team
        self.away_team = away_team
        self.week = week

    def __str__(self):
        return f"Week {self.week}: {self.away_team.name} @ {self.home_team.name}"

    def to_dict(self):
        return {
            "home_team": self.home_team.name,
            "away_team": self.away_team.name
        }

class Schedule:
    def __init__(self):
        self.games = []
 
    def add_game(self, game):
        self.games.append(game)

    def get_team_schedule(self, team):
        return [game for game in self.games if game.home_team == team or game.away_team == team]

    def __str__(self):
        return "\n".join(str(game) for game in self.games)

    def to_dict(self):
        schedule_dict = {}
        for game in self.games:
            week = f"Week {game.week}"
            if week not in schedule_dict:
                schedule_dict[week] = []
            schedule_dict[week].append(game.to_dict())
        return schedule_dict

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def get_team_schedule_dict(self, team, bye_week):
        team_games = self.get_team_schedule(team)
        schedule = {}
        for week in range(1, TOTAL_WEEKS + 1):
            if week == bye_week:
                schedule[f"Week {week}"] = {"bye_week": True}
            else:
                game = next((g for g in team_games if g.week == week), None)
                if game:
                    schedule[f"Week {week}"] = {
                        "opponent": game.away_team.name if game.home_team == team else game.home_team.name,
                        "is_home": game.home_team == team
                    }
        return {
            "team": team.name,
            "conference": team.conference,
            "division": team.division,
            "schedule": schedule
        }

    def save_team_schedules(self, output_dir, bye_weeks):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for team in set([game.home_team for game in self.games] + [game.away_team for game in self.games]):
            team_schedule = self.get_team_schedule_dict(team, bye_weeks[team])
            filename = os.path.join(output_dir, f"{team.name.replace(' ', '_').lower()}_schedule.json")
            with open(filename, 'w') as f:
                json.dump(team_schedule, f, indent=2)
        
        return len(set([game.home_team for game in self.games] + [game.away_team for game in self.games]))
