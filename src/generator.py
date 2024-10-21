import random
from .team import Team
from .schedule import Game, Schedule
from .teams import NFL_TEAMS, get_all_teams, get_team_info

class ScheduleGenerator:
    def __init__(self):
        self.teams = self._create_teams()
        self.schedule = Schedule()
        self.num_weeks = 18 # 18-week season

    def _create_teams(self):
        teams = []
        for team_name in get_all_teams():
            conference, division = get_team_info(team_name)
            teams.append(Team(team_name, division, conference))
        return teams

    def generate_schedule(self):
        # This is a simplified schedule generation. A real NFL schedule is more complex.
        for week in range(1, self.num_weeks+1):  
            teams_this_week = self.teams.copy()
            random.shuffle(teams_this_week)
            while teams_this_week:
                home_team = teams_this_week.pop()
                away_team = teams_this_week.pop()
                game = Game(home_team, away_team, week)
                self.schedule.add_game(game)

    def get_schedule(self):
        return self.schedule
