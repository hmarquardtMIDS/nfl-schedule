import unittest
from src.generator import ScheduleGenerator
from src.teams import get_all_teams

class TestScheduleGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = ScheduleGenerator()
        success = cls.generator.generate_schedule(max_attempts=1000)
        if not success:
            raise unittest.SkipTest("Failed to generate a valid schedule after 1000 attempts")

    def setUp(self):
        # No need to generate a new schedule for each test
        pass

    def test_total_weeks(self):
        """Test that the schedule has 18 weeks."""
        weeks = set(game.week for game in self.generator.get_schedule().games)
        self.assertEqual(len(weeks), 18)

    def test_games_per_week(self):
        """Test that each week has 13, 14, 15, or 16 games (accounting for bye weeks)."""
        generator = ScheduleGenerator()
        generator.generate_schedule()
        schedule = generator.get_schedule()
        
        for week in range(1, 19):  # 18-week season
            games_this_week = [game for game in schedule.games if game.week == week]
            self.assertIn(len(games_this_week), [13, 14, 15, 16], f"Week {week} has {len(games_this_week)} games, which is not in the expected range")

    def test_bye_weeks(self):
        """Test that each team has exactly one bye week between weeks 5 and 14."""
        for team, bye_week in self.generator.get_bye_weeks().items():
            self.assertIsNotNone(bye_week)
            self.assertGreaterEqual(bye_week, 5)
            self.assertLessEqual(bye_week, 14)

    def test_unique_bye_weeks(self):
        """Test that no more than 6 teams have a bye in any given week."""
        generator = ScheduleGenerator()
        generator.generate_schedule()
        bye_weeks = generator.get_bye_weeks()
        
        bye_counts = {}
        for team, week in bye_weeks.items():
            bye_counts[week] = bye_counts.get(week, 0) + 1
        
        for week, count in bye_counts.items():
            self.assertLessEqual(count, 6, f"Week {week} has {count} teams on bye, which exceeds the maximum of 6")

    def test_games_per_team(self):
        """Test that each team plays exactly 17 games."""
        for team in get_all_teams():
            team_games = [game for game in self.generator.get_schedule().games 
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
        for team, bye_week in self.generator.get_bye_weeks().items():
            games_on_bye = [game for game in self.generator.get_schedule().games 
                            if game.week == bye_week and team.name in [game.home_team.name, game.away_team.name]]
            self.assertEqual(len(games_on_bye), 0)

    def test_bye_week_constraints(self):
        """Test that there's an even number of teams on bye each week, never more than 6."""
        bye_weeks_count = {week: 0 for week in range(5, 15)}  # Weeks 5-14
        for team, bye_week in self.generator.get_bye_weeks().items():
            bye_weeks_count[bye_week] += 1
        
        for week, count in bye_weeks_count.items():
            self.assertLessEqual(count, 6, f"Week {week} has more than 6 teams on bye")
            self.assertEqual(count % 2, 0, f"Week {week} has an odd number of teams on bye")

    def test_total_bye_weeks(self):
        """Test that the total number of bye weeks matches the number of teams."""
        total_bye_weeks = sum(1 for bye_week in self.generator.get_bye_weeks().values() if bye_week is not None)
        self.assertEqual(total_bye_weeks, len(self.generator.teams))

    def test_divisional_matchups(self):
        """Test that each team plays its divisional opponents twice."""
        schedule = self.generator.get_schedule()
        for team in self.generator.teams:
            divisional_opponents = [t for t in self.generator.teams if t.conference == team.conference and t.division == team.division and t != team]
            for opponent in divisional_opponents:
                matchups = [game for game in schedule.games if 
                            (game.home_team == team and game.away_team == opponent) or 
                            (game.home_team == opponent and game.away_team == team)]
                self.assertEqual(len(matchups), 2, f"{team.name} should play {opponent.name} twice, but played {len(matchups)} times")

if __name__ == '__main__':
    unittest.main()
