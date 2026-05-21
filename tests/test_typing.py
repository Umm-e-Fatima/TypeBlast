import unittest # Import the unittest module from the standard library to write and run test cases
import time # Import the time module to simulate delays during typing speed tests
from typing_session import TypingSession, TypingException # Import the session class and custom exception to test
from typing_text import TextBank # Import the TextBank class to test text retrieval

class TestTypingBlast(unittest.TestCase): # Define a test case class inheriting from unittest.TestCase
    def setUp(self): # Define the setUp method that runs automatically before every single test
        self.target = "Hello World" # Set a simple target string for testing purposes
        self.session = TypingSession(self.target) # Initialize a fresh TypingSession instance before each test method

    def test_session_creation(self): # Define test method to verify correct initialization state
        self.assertEqual(self.session.target_text, self.target) # Check that the target text was stored correctly
        self.assertIsNone(self.session.start_time) # Check that start_time is initially None
        self.assertFalse(self.session.is_active) # Check that the session is not active by default

    def test_session_start(self): # Define test method to verify state changes when session begins
        self.session.start() # Call the start method on the test session
        self.assertTrue(self.session.is_active) # Verify that the session is now marked as active
        self.assertIsNotNone(self.session.start_time) # Verify that a start time has been recorded

    def test_session_already_started(self): # Define test method to ensure double-starting raises an error
        self.session.start() # Call the start method to begin the session
        with self.assertRaises(TypingException): # Expect a TypingException to be raised in the following block
            self.session.start() # Attempt to start the session a second time, triggering the exception

    def test_session_stop(self): # Define test method to verify state changes when session ends
        self.session.start() # Call the start method so the session becomes active
        self.session.stop() # Call the stop method to end the active session
        self.assertFalse(self.session.is_active) # Verify that the session is no longer marked as active
        self.assertIsNotNone(self.session.end_time) # Verify that an end time has been recorded

    def test_session_stop_without_start(self): # Define test method to ensure stopping an inactive session raises an error
        with self.assertRaises(TypingException): # Expect a TypingException to be raised in the following block
            self.session.stop() # Attempt to stop a session that was never started

    def test_get_wpm_perfect(self): # Define test method to verify WPM calculation works with realistic data
        self.session.start() # Start the typing session to begin timing
        time.sleep(1) # Simulate a human typing delay by sleeping for 1 second
        self.session.stop() # Stop the session to end the timing
        wpm = self.session.get_wpm("Hello World") # Calculate the WPM for typing the target text
        self.assertGreater(wpm, 0.0) # Assert that the calculated WPM is a float strictly greater than 0

    def test_get_accuracy_perfect(self): # Define test method to verify 100% accuracy calculation
        accuracy = self.session.get_accuracy("Hello World") # Calculate accuracy for perfectly matching text
        self.assertEqual(accuracy, 100.0) # Assert that the returned accuracy is exactly 100.0 percent

    def test_get_accuracy_partial(self): # Define test method to verify partial accuracy calculation
        accuracy = self.session.get_accuracy("Hello Worlx") # Calculate accuracy for text with one typo
        self.assertGreater(accuracy, 0.0) # Assert that accuracy is greater than 0
        self.assertLess(accuracy, 100.0) # Assert that accuracy is strictly less than 100.0 percent

    def test_get_results_keys(self): # Define test method to verify get_results returns a comprehensive dictionary
        self.session.start() # Start the session to populate time metrics
        self.session.stop() # Stop the session immediately to complete it
        results = self.session.get_results("Hello World") # Fetch the full results dictionary from the session
        self.assertIn("wpm", results) # Check that the 'wpm' key exists in the results dictionary
        self.assertIn("accuracy", results) # Check that the 'accuracy' key exists in the results dictionary
        self.assertIn("elapsed_time", results) # Check that the 'elapsed_time' key exists in the results dictionary
        self.assertIn("correct_chars", results) # Check that the 'correct_chars' key exists in the results dictionary
        self.assertIn("total_chars", results) # Check that the 'total_chars' key exists in the results dictionary

    def test_textbank_get_random(self): # Define test method to verify TextBank functionality
        random_text = TextBank.get_random() # Call the get_random class method to retrieve a paragraph
        self.assertGreater(len(random_text), 0) # Verify that the returned string is not empty
        self.assertIn(random_text, TextBank.PARAGRAPHS) # Verify that the returned string belongs to the predefined list

if __name__ == '__main__': # Check if this test file is being run directly as a script
    unittest.main() # Run all the defined test cases using the unittest framework
