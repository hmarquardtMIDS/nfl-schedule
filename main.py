from src.generator import ScheduleGenerator
import os

import unittest
import os
from src.generator import ScheduleGenerator

def run_tests():
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def generate_schedule():
    generator = ScheduleGenerator()
    generator.generate_schedule()
    schedule = generator.get_schedule()
    bye_weeks = generator.get_bye_weeks()
    
    print("Full NFL Schedule:")
    print(schedule)
    
    print("\nSchedule for AFC North Team (Cincinnati Bengals):")
    sample_team = next(team for team in generator.teams if team.name == "Cincinnati Bengals")
    team_schedule = schedule.get_team_schedule(sample_team)
    team_bye_week = bye_weeks[sample_team]
    
    for week in range(1, 19):  # 18-week season
        if week == team_bye_week:
            print(f"Week {week}: BYE")
        else:
            game = next((g for g in team_schedule if g.week == week), None)
            if game:
                opponent = game.away_team if game.home_team == sample_team else game.home_team
                location = "vs" if game.home_team == sample_team else "@"
                print(f"Week {week}: {location} {opponent.name}")
            else:
                print(f"Week {week}: No game scheduled (error)")

    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the full schedule to a JSON file
    json_filename = os.path.join(output_dir, "nfl_schedule.json")
    schedule.save_to_json(json_filename)
    print(f"\nFull schedule saved to {json_filename}")

    # Save individual team schedules
    team_schedules_dir = os.path.join(output_dir, "team_schedules")
    num_teams = schedule.save_team_schedules(team_schedules_dir, bye_weeks)
    print(f"{num_teams} individual team schedules saved to {team_schedules_dir}")

    # Save bye week summary
    bye_week_summary_filename = os.path.join(output_dir, "bye_week_summary.json")
    schedule.save_bye_week_summary(bye_week_summary_filename, bye_weeks)
    print(f"Bye week summary saved to {bye_week_summary_filename}")

def main():
    print("Running tests...")
    tests_passed = run_tests()
    
    if tests_passed:
        print("\nAll tests passed. Generating schedule...\n")
        generate_schedule()
    else:
        print("\nTests failed. Please fix the issues before generating the schedule.")

if __name__ == "__main__":
    main()
