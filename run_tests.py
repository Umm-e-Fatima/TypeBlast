import unittest # Import the unittest module from the standard library to load and run tests
import os # Import the os module for handling file and directory paths safely
import sys # Import the sys module to handle the script exit code based on test success
from datetime import datetime # Import datetime class to generate timestamps for the test report

def run_all_tests(): # Define the main function that will discover and execute all test cases
    loader = unittest.TestLoader() # Instantiate a TestLoader object to find test files automatically
    start_dir = os.path.join(os.getcwd(), "tests") # Construct the absolute directory path where the test files are located
    suite = loader.discover(start_dir) # Use the loader to automatically discover and load tests from the directory
    
    runner = unittest.TextTestRunner(verbosity=2) # Instantiate a TextTestRunner with verbosity level 2 for detailed output
    result = runner.run(suite) # Execute the test suite using the runner and store the returned TestResult object
    
    total_run = result.testsRun # Retrieve the total number of tests that were executed during the run
    total_errors = len(result.errors) # Calculate the total number of tests that encountered unexpected runtime errors
    total_failures = len(result.failures) # Calculate the total number of tests that failed their explicit assertions
    total_passed = total_run - total_errors - total_failures # Calculate the total number of tests that successfully passed
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Generate a formatted string of the current date and time
    
    summary_lines = [ # Create a list to hold all the string lines of the formatted summary report
        f"Test Report - {current_time}", # Add the timestamp line as the title header of the text report
        "-" * 30, # Add a horizontal dash separator line for better visual readability
        f"Total tests run: {total_run}", # Add a line stating the overall total number of tests executed
        f"Tests passed: {total_passed}", # Add a line stating the total number of tests that passed successfully
        f"Tests failed: {total_failures}", # Add a line stating the total number of tests that explicitly failed
        f"Tests with errors: {total_errors}", # Add a line stating the total number of tests that threw unexpected errors
        "-" * 30 # Add a closing horizontal dash separator line at the bottom of the summary
    ] # Close the list definition for the summary lines
    
    for line in summary_lines: # Loop over each string line in the constructed summary list array
        print(line) # Print the current summary line to the standard console output for the user to read
        
    report_path = os.path.join(os.getcwd(), "test_report.txt") # Construct the absolute file path where the report should be saved
    with open(report_path, "w") as file: # Open the target file in write mode using a context manager to ensure safe closing
        for line in summary_lines: # Loop over each string line in the summary list once again to write to the file
            file.write(line + "\n") # Write the current string line followed by a newline character directly to the open file
            
    if not result.wasSuccessful(): # Check if any test encountered an error or a failure during execution
        sys.exit(1) # Exit the script with a non-zero status code to indicate the test suite failed
    sys.exit(0) # Exit the script with a zero status code to indicate the test suite completely passed

if __name__ == "__main__": # Check if this script is being executed directly rather than being imported elsewhere
    run_all_tests() # Call the main run_all_tests function to initiate the test discovery and execution
