import random
from .team import Team
from .schedule import Game, Schedule
from .teams import NFL_TEAMS, get_all_teams, get_team_info

class ScheduleGenerator:
    def __init__(self):
        self.teams = self._create_teams()
        self.schedule = Schedule()
        self.bye_weeks = {team: None for team in self.teams}

    def _create_teams(self):
        teams = []
        for team_name in get_all_teams():
            conference, division = get_team_info(team_name)
            teams.append(Team(team_name, division, conference))
        return teams

    def _assign_bye_weeks(self):
        bye_week_range = list(range(5, 15))  # Weeks 5 through 14
        teams_to_assign = self.teams.copy()
        random.shuffle(teams_to_assign)

        for week in bye_week_range:
            if not teams_to_assign:
                break
            teams_on_bye = random.sample(teams_to_assign, min(4, len(teams_to_assign)))
            for team in teams_on_bye:
                self.bye_weeks[team] = week
                teams_to_assign.remove(team)

    def generate_schedule(self):
        self._assign_bye_weeks()

        for week in range(1, 19):  # 18-week season
            teams_this_week = [team for team in self.teams if self.bye_weeks[team] != week]
            random.shuffle(teams_this_week)
            
            while len(teams_this_week) >= 2:
                home_team = teams_this_week.pop()
                away_team = teams_this_week.pop()
                game = Game(home_team, away_team, week)
                self.schedule.add_game(game)

    def get_schedule(self):
        return self.schedule

    def get_bye_weeks(self):
        return self.bye_weeks
