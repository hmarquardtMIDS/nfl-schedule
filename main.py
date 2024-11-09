from src.generator import ScheduleGenerator
import os
import unittest

def run_tests():
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def generate_schedule():
    generator = ScheduleGenerator()
    schedule, bye_weeks = generator.generate_schedule()
    
    if not schedule or not bye_weeks:
        print("Failed to generate a valid schedule. Please try again.")
        return

    print("Full NFL Schedule:")
    print(schedule)
    
    # ... (rest of the function remains unchanged)


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
