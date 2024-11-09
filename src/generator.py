import random
from .team import Team
from .schedule import Game, Schedule
from .teams import NFL_TEAMS, get_all_teams, get_team_info

class ScheduleGenerator:
    def __init__(self):
        self.teams = self._create_teams()
        self.schedule = None
        self.bye_weeks = None

    def _create_teams(self):
        teams = []
        for team_name in get_all_teams():
            conference, division = get_team_info(team_name)
            teams.append(Team(team_name, division, conference))
        return teams

    def generate_schedule(self, max_attempts=1000):
        for attempt in range(max_attempts):
            try:
                self.schedule = Schedule()
                self.bye_weeks = self._assign_bye_weeks()
                self._schedule_all_games()
                if self._verify_schedule():
                    print(f"Valid schedule generated after {attempt + 1} attempts.")
                    return True
            except ValueError as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
        
        print(f"Failed to generate a valid schedule after {max_attempts} attempts.")
        return False

    def _assign_bye_weeks(self):
        bye_weeks = {team: None for team in self.teams}
        bye_week_range = list(range(5, 15))  # Weeks 5 through 14
        teams_to_assign = self.teams.copy()
        random.shuffle(teams_to_assign)

        for week in bye_week_range:
            teams_on_bye = teams_to_assign[:4]  # Assign 4 teams per week
            for team in teams_on_bye:
                bye_weeks[team] = week
                teams_to_assign.remove(team)

        return bye_weeks

    def _schedule_all_games(self):
        self._schedule_divisional_games()
        self._schedule_conference_games()
        self._schedule_interconference_games()

    def _schedule_divisional_games(self):
        for conference in NFL_TEAMS.keys():
            for division in NFL_TEAMS[conference].keys():
                teams = [team for team in self.teams if team.conference == conference and team.division == division]
                for i, home_team in enumerate(teams):
                    for away_team in teams[i+1:]:
                        self._schedule_game(home_team, away_team)
                        self._schedule_game(away_team, home_team)

    def _schedule_conference_games(self):
        # Implement conference game scheduling logic here
        pass

    def _schedule_interconference_games(self):
        # Implement interconference game scheduling logic here
        pass

    def _schedule_game(self, home_team, away_team):
        available_weeks = self._find_available_weeks(home_team, away_team)
        if not available_weeks:
            raise ValueError(f"Unable to schedule game between {home_team.name} and {away_team.name}")
        
        week = random.choice(available_weeks)
        game = Game(home_team, away_team, week)
        self.schedule.add_game(game)

    def _find_available_weeks(self, home_team, away_team):
        return [week for week in range(1, 19) 
                if self.bye_weeks[home_team] != week 
                and self.bye_weeks[away_team] != week 
                and not any(game.week == week and (game.home_team == home_team or game.away_team == home_team) for game in self.schedule.games)
                and not any(game.week == week and (game.home_team == away_team or game.away_team == away_team) for game in self.schedule.games)]

    def _verify_schedule(self):
        # Implement thorough schedule verification here
        # Check for correct number of games, divisional matchups, etc.
        return True  # Placeholder, implement actual verification

    def get_schedule(self):
        return self.schedule

    def get_bye_weeks(self):
        return self.bye_weeks
