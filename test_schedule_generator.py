import unittest
from src.generator import ScheduleGenerator
from src.teams import get_all_teams

class TestScheduleGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ScheduleGenerator()
        self.generator.generate_schedule()
        self.schedule = self.generator.get_schedule()
        self.bye_weeks = self.generator.get_bye_weeks()

    def test_total_weeks(self):
        """Test that the schedule has 18 weeks."""
        weeks = set(game.week for game in self.schedule.games)
        self.assertEqual(len(weeks), 18)

    def test_games_per_week(self):
        """Test that each week has 16 games (except for bye weeks)."""
        for week in range(1, 19):
            games_this_week = [game for game in self.schedule.games if game.week == week]
            if 5 <= week <= 14:
                self.assertIn(len(games_this_week), [14, 15, 16])  # Accounting for bye weeks
            else:
                self.assertEqual(len(games_this_week), 16)

    def test_bye_weeks(self):
        """Test that each team has exactly one bye week between weeks 5 and 14."""
        for team, bye_week in self.bye_weeks.items():
            self.assertIsNotNone(bye_week)
            self.assertGreaterEqual(bye_week, 5)
            self.assertLessEqual(bye_week, 14)

    def test_unique_bye_weeks(self):
        """Test that no more than 4 teams have a bye in any given week."""
        bye_week_counts = {}
        for bye_week in self.bye_weeks.values():
            bye_week_counts[bye_week] = bye_week_counts.get(bye_week, 0) + 1

        for week, count in bye_week_counts.items():
            self.assertLessEqual(count, 4)

    def test_games_per_team(self):
        """Test that each team plays exactly 17 games."""
        for team in get_all_teams():
            team_games = [game for game in self.schedule.games 
                          if team in [game.home_team.name, game.away_team.name]]
            self.assertEqual(len(team_games), 17)

    # def test_no_duplicate_games(self):
    #     """Test that there are no duplicate games in the schedule."""
    #     game_pairs = set()
    #     for game in self.schedule.games:
    #         game_pair = frozenset([game.home_team.name, game.away_team.name])
    #         self.assertNotIn(game_pair, game_pairs)
    #         game_pairs.add(game_pair)

    def test_no_games_on_bye_weeks(self):
        """Test that teams don't play games during their bye week."""
        for team, bye_week in self.bye_weeks.items():
            games_on_bye = [game for game in self.schedule.games 
                            if game.week == bye_week and team.name in [game.home_team.name, game.away_team.name]]
            self.assertEqual(len(games_on_bye), 0)

if __name__ == '__main__':
    unittest.main()
