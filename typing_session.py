import time # Import the time module from the standard library to measure session duration

class TypingException(Exception): # Define a custom exception class that inherits from the base Exception class
    pass # Use 'pass' as this exception class does not require any additional custom behavior or methods

class TypingSession: # Define the TypingSession class to manage the state and calculations of a typing test
    def __init__(self, target_text): # Define the constructor method that takes 'target_text' as an argument
        self.target_text = target_text # Store the provided target text in the 'target_text' instance attribute
        self.start_time = None # Initialize the 'start_time' attribute to None, indicating the session hasn't started
        self.end_time = None # Initialize the 'end_time' attribute to None, indicating the session hasn't ended
        self.is_active = False # Initialize the 'is_active' boolean flag to False

    def start(self): # Define the start method to begin the typing session
        if self.is_active: # Check if the 'is_active' flag is currently True
            raise TypingException("Session already started") # Raise a TypingException if the session is already active
        self.is_active = True # Set the 'is_active' flag to True to mark the session as started
        self.start_time = time.time() # Record the current system time using time.time() and store it in 'start_time'

    def stop(self): # Define the stop method to end the active typing session
        if not self.is_active: # Check if the 'is_active' flag is currently False
            raise TypingException("Session not active") # Raise a TypingException if the session hasn't been started
        self.end_time = time.time() # Record the current system time using time.time() and store it in 'end_time'
        self.is_active = False # Set the 'is_active' flag back to False to indicate the session has ended

    def get_elapsed_time(self): # Define a method to calculate the total elapsed time of the completed session
        if self.start_time is None or self.end_time is None: # Check if either the start time or end time is missing
            return 0.0 # Return 0.0 if the session has not been properly completed
        elapsed = self.end_time - self.start_time # Calculate the difference between end time and start time
        return round(elapsed, 2) # Return the calculated elapsed time rounded to 2 decimal places

    def get_wpm(self, typed_text): # Define a method to calculate the Words Per Minute based on the typed text
        if self.start_time is None or self.end_time is None: # Check if the session is not yet complete
            return 0.0 # Return 0.0 if the session is not complete
        elapsed_time = self.get_elapsed_time() # Retrieve the elapsed time in seconds using the get_elapsed_time method
        if elapsed_time == 0: # Prevent division by zero if the elapsed time is exactly 0 seconds
            return 0.0 # Return 0.0 to avoid a ZeroDivisionError
        minutes = elapsed_time / 60.0 # Convert the elapsed time from seconds into minutes
        words = len(typed_text) / 5.0 # Estimate the number of words by dividing the character count by 5
        wpm = words / minutes # Calculate WPM by dividing the estimated word count by the elapsed time in minutes
        return round(wpm, 2) # Return the calculated WPM rounded to 2 decimal places

    def get_accuracy(self, typed_text): # Define a method to calculate typing accuracy by comparing to target text
        if not self.target_text: # Check if the target text is empty to prevent division by zero
            return 0.0 # Return 0.0 if there is no target text to compare against
        total_chars = len(self.target_text) # Determine the total number of characters in the target text
        correct_chars = 0 # Initialize a counter variable to keep track of correctly typed characters
        for i in range(min(len(typed_text), total_chars)): # Loop through the indices up to the length of the shorter string
            if typed_text[i] == self.target_text[i]: # Check if the character at the current index matches the target
                correct_chars += 1 # Increment the correct_chars counter if the characters match exactly
        accuracy = (correct_chars / total_chars) * 100.0 # Calculate the accuracy percentage based on total characters
        return round(accuracy, 2) # Return the calculated accuracy rounded to 2 decimal places

    def get_results(self, typed_text): # Define a method to compile all the session metrics into a single dictionary
        total_chars = len(self.target_text) # Retrieve the total number of characters from the target text length
        correct_chars = 0 # Initialize a counter for correctly typed characters
        for i in range(min(len(typed_text), total_chars)): # Loop through the indices to count correct characters
            if typed_text[i] == self.target_text[i]: # Compare the character at the current index in both strings
                correct_chars += 1 # Increment the correct_chars counter if they match
        return { # Begin defining and returning the results dictionary
            "wpm": self.get_wpm(typed_text), # Add the calculated Words Per Minute metric to the dictionary
            "accuracy": self.get_accuracy(typed_text), # Add the calculated accuracy percentage to the dictionary
            "elapsed_time": self.get_elapsed_time(), # Add the calculated total elapsed time to the dictionary
            "correct_chars": correct_chars, # Add the total number of correctly typed characters to the dictionary
            "total_chars": total_chars # Add the total number of characters in the target text to the dictionary
        } # Close the dictionary structure and complete the return statement
