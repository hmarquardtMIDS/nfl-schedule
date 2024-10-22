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

        bye_weeks_count = {week: 0 for week in bye_week_range}

        while teams_to_assign:
            available_weeks = [week for week in bye_week_range if bye_weeks_count[week] < 6]
            if not available_weeks:
                # If we can't assign all byes, start over
                return self._assign_bye_weeks()

            week = random.choice(available_weeks)
            teams_on_bye = random.sample(teams_to_assign, min(2, len(teams_to_assign)))
            
            for team in teams_on_bye:
                self.bye_weeks[team] = week
                teams_to_assign.remove(team)
            
            bye_weeks_count[week] += 2

    def _generate_divisional_games(self):
        divisional_games = []
        for conference in NFL_TEAMS.keys():
            for division in NFL_TEAMS[conference].keys():
                teams = [team for team in self.teams if team.conference == conference and team.division == division]
                for home_team in teams:
                    for away_team in teams:
                        if home_team != away_team:
                            # Create two games, one home and one away
                            divisional_games.append((home_team, away_team))
                            divisional_games.append((away_team, home_team))
        return divisional_games

    def generate_schedule(self):
        self._assign_bye_weeks()
        divisional_games = self._generate_divisional_games()
        
        # Shuffle the divisional games to distribute them throughout the season
        random.shuffle(divisional_games)

        # Create a list of all possible game slots
        game_slots = [(week, team) for week in range(1, 19) for team in self.teams if self.bye_weeks[team] != week]
        
        # Assign divisional games first
        for home_team, away_team in divisional_games:
            home_slots = [slot for slot in game_slots if slot[1] == home_team]
            away_slots = [slot for slot in game_slots if slot[1] == away_team]
            common_weeks = set(slot[0] for slot in home_slots) & set(slot[0] for slot in away_slots)
            
            if not common_weeks:
                raise ValueError("Unable to schedule all divisional games")
            
            week = random.choice(list(common_weeks))
            game = Game(home_team, away_team, week)
            self.schedule.add_game(game)
            
            # Remove used slots
            game_slots = [slot for slot in game_slots if slot != (week, home_team) and slot != (week, away_team)]

        # Fill in the rest of the schedule with non-divisional games
        while game_slots:
            week, home_team = game_slots.pop(random.randint(0, len(game_slots) - 1))
            available_away_teams = [slot[1] for slot in game_slots if slot[0] == week and slot[1].conference == home_team.conference]
            
            if not available_away_teams:
                available_away_teams = [slot[1] for slot in game_slots if slot[0] == week]
            
            if not available_away_teams:
                raise ValueError("Unable to complete the schedule")
            
            away_team = random.choice(available_away_teams)
            game = Game(home_team, away_team, week)
            self.schedule.add_game(game)
            
            # Remove the used away team slot
            game_slots = [slot for slot in game_slots if slot != (week, away_team)]

    def get_schedule(self):
        return self.schedule

    def get_bye_weeks(self):
        return self.bye_weeks
