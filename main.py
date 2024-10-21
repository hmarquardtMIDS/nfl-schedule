from src.generator import ScheduleGenerator
import os

def main():
    generator = ScheduleGenerator()
    generator.generate_schedule()
    schedule = generator.get_schedule()
    
    print("Full NFL Schedule:")
    print(schedule)
    
    print("\nSchedule for AFC East Team (Buffalo Bills):")
    team_schedule = schedule.get_team_schedule(generator.teams[0])
    for game in team_schedule:
        print(game)

    # Save the schedule to a JSON file
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    json_filename = os.path.join(output_dir, "nfl_schedule.json")
    schedule.save_to_json(json_filename)
    print(f"\nSchedule saved to {json_filename}")

if __name__ == "__main__":
    main()
