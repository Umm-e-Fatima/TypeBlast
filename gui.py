import tkinter as tk # Import the main tkinter module for GUI creation
from tkinter import ttk # Import themed tk widgets as requested by user
import tkinter.messagebox # Import messagebox for showing result popups
import time # Import the time module as requested by the user
from typing_session import TypingSession, TypingException # Import the custom session and exception classes
from typing_text import TextBank # Import the TextBank class to retrieve typing texts

class TypeBlastApp: # Define the main application class for the TypeBlast GUI
    def __init__(self, root): # Initialize the app with the root Tk window
        self.root = root # Store the root window reference
        self.root.title("TypeBlast ⌨️ — Typing Speed Tester") # Set the window title
        self.root.geometry("750x620") # Set the exact window dimensions requested
        self.root.resizable(False, False) # Disable window resizing to maintain layout
        self.root.configure(bg="#1e1e2e") # Set the dark purple-black background color
        
        screen_width = self.root.winfo_screenwidth() # Get the user's screen width
        screen_height = self.root.winfo_screenheight() # Get the user's screen height
        x_coordinate = int((screen_width / 2) - (750 / 2)) # Calculate the X coordinate for centering
        y_coordinate = int((screen_height / 2) - (620 / 2)) # Calculate the Y coordinate for centering
        self.root.geometry(f"750x620+{x_coordinate}+{y_coordinate}") # Apply the geometry with coordinates
        
        self.session = None # Initialize the typing session reference to None
        self.current_text = TextBank.get_random() # Get an initial random text from the TextBank
        
        self.create_widgets() # Call the method to build all GUI components
        self.setup_tags() # Call the method to configure text tags for coloring
        self.reset_ui() # Set initial UI state by calling reset_ui

    def create_widgets(self): # Define method to construct the GUI elements
        self.header_label = tk.Label(self.root, text="⌨️ TypeBlast", font=("Courier", 26, "bold"), fg="#cba6f7", bg="#1e1e2e") # Create the main title label
        self.header_label.pack(pady=(20, 0)) # Pack the title with some top padding
        
        self.subtitle_label = tk.Label(self.root, text="Test Your Typing Speed & Accuracy", font=("Courier", 10), fg="#6c7086", bg="#1e1e2e") # Create the subtitle label
        self.subtitle_label.pack(pady=(5, 15)) # Pack the subtitle with padding
        
        self.separator = tk.Frame(self.root, height=2, bg="#cba6f7") # Create a thin separator frame
        self.separator.pack(fill=tk.X, padx=30, pady=5) # Pack the separator to fill horizontally
        
        self.target_frame = tk.Frame(self.root, bg="#1e1e2e") # Create a frame for the target text section
        self.target_frame.pack(fill=tk.X, padx=30, pady=(15, 5)) # Pack the target frame
        
        self.target_lbl = tk.Label(self.target_frame, text="📋 Your Text to Type:", fg="#cba6f7", bg="#1e1e2e", font=("Courier", 11, "bold")) # Create label for target text
        self.target_lbl.pack(anchor=tk.W, pady=(0, 5)) # Pack label aligned to the left
        
        self.target_text_widget = tk.Text(self.target_frame, bg="#313244", fg="#cdd6f4", font=("Courier", 12), height=4, width=70, relief="flat", padx=10, pady=8, wrap=tk.WORD, state=tk.DISABLED) # Create read-only Text widget for target text
        self.target_text_widget.pack() # Pack the target text widget
        
        self.typing_frame = tk.Frame(self.root, bg="#1e1e2e") # Create a frame for the typing area
        self.typing_frame.pack(fill=tk.X, padx=30, pady=(15, 10)) # Pack the typing frame
        
        self.typing_lbl = tk.Label(self.typing_frame, text="✍️ Start Typing Below:", fg="#cba6f7", bg="#1e1e2e", font=("Courier", 11, "bold")) # Create label for typing area
        self.typing_lbl.pack(anchor=tk.W, pady=(0, 5)) # Pack label aligned to the left
        
        self.typing_text_widget = tk.Text(self.typing_frame, bg="#313244", fg="#ffffff", font=("Courier", 12), insertbackground="#cba6f7", height=4, width=70, relief="flat", padx=10, pady=8, wrap=tk.WORD) # Create Text widget for user typing
        self.typing_text_widget.pack() # Pack the typing text widget
        self.typing_text_widget.bind("<KeyRelease>", self.on_key_release) # Bind key release event to live highlighting method
        
        self.btn_frame = tk.Frame(self.root, bg="#1e1e2e") # Create a frame for the buttons
        self.btn_frame.pack(pady=15) # Pack the buttons frame
        
        self.start_btn = tk.Button(self.btn_frame, text="🚀 Start Test", command=self.start_test, bg="#cba6f7", fg="#1e1e2e", font=("Courier", 11, "bold"), relief="flat", padx=12, pady=6, cursor="hand2") # Create Start Test button
        self.start_btn.pack(side=tk.LEFT, padx=10) # Pack start button to the left
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#b4befe")) # Add hover enter effect
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg="#cba6f7")) # Add hover leave effect
        
        self.stop_btn = tk.Button(self.btn_frame, text="⏹ Stop & Results", command=self.stop_test, bg="#cba6f7", fg="#1e1e2e", font=("Courier", 11, "bold"), relief="flat", padx=12, pady=6, cursor="hand2") # Create Stop & Results button
        self.stop_btn.pack(side=tk.LEFT, padx=10) # Pack stop button next to start button
        self.stop_btn.bind("<Enter>", lambda e: self.stop_btn.config(bg="#b4befe")) # Add hover enter effect
        self.stop_btn.bind("<Leave>", lambda e: self.stop_btn.config(bg="#cba6f7")) # Add hover leave effect
        
        self.new_btn = tk.Button(self.btn_frame, text="🔄 New Text", command=self.new_text, bg="#cba6f7", fg="#1e1e2e", font=("Courier", 11, "bold"), relief="flat", padx=12, pady=6, cursor="hand2") # Create New Text button
        self.new_btn.pack(side=tk.LEFT, padx=10) # Pack new text button to the right
        self.new_btn.bind("<Enter>", lambda e: self.new_btn.config(bg="#b4befe")) # Add hover enter effect
        self.new_btn.bind("<Leave>", lambda e: self.new_btn.config(bg="#cba6f7")) # Add hover leave effect
        
        self.results_frame = tk.Frame(self.root, bg="#313244", padx=15, pady=10) # Create a frame for the results
        self.results_frame.pack(fill=tk.X, padx=30, pady=15) # Pack the results frame
        
        self.time_lbl = tk.Label(self.results_frame, text="⏱ Time: --s", fg="#cdd6f4", font=("Courier", 11, "bold"), bg="#313244") # Create time result label
        self.time_lbl.pack(side=tk.LEFT, expand=True) # Pack time label with expansion
        
        self.wpm_lbl = tk.Label(self.results_frame, text="🚀 WPM: --", fg="#cdd6f4", font=("Courier", 11, "bold"), bg="#313244") # Create WPM result label
        self.wpm_lbl.pack(side=tk.LEFT, expand=True) # Pack WPM label with expansion
        
        self.acc_lbl = tk.Label(self.results_frame, text="🎯 Accuracy: --%", fg="#cdd6f4", font=("Courier", 11, "bold"), bg="#313244") # Create accuracy result label
        self.acc_lbl.pack(side=tk.LEFT, expand=True) # Pack accuracy label with expansion
        
        self.correct_lbl = tk.Label(self.results_frame, text="✅ Correct: --", fg="#cdd6f4", font=("Courier", 11, "bold"), bg="#313244") # Create correct chars result label
        self.correct_lbl.pack(side=tk.LEFT, expand=True) # Pack correct label with expansion
        
        self.status_bar = tk.Label(self.root, text="⌨️ Click 'Start Test' to begin...", bg="#181825", fg="#cba6f7", font=("Courier", 9), pady=5) # Create the status bar label at the bottom
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X) # Pack status bar at the bottom

    def setup_tags(self): # Define method to configure text tags for highlighting
        self.typing_text_widget.tag_config("correct", foreground="#a6e3a1") # Configure 'correct' tag with green foreground
        self.typing_text_widget.tag_config("wrong", foreground="#f38ba8") # Configure 'wrong' tag with red foreground

    def update_target_display(self): # Define method to update the target text widget
        self.target_text_widget.config(state=tk.NORMAL) # Enable widget to modify text
        self.target_text_widget.delete("1.0", tk.END) # Clear existing text
        self.target_text_widget.insert("1.0", self.current_text) # Insert the new target text
        self.target_text_widget.config(state=tk.DISABLED) # Disable widget to prevent user edits

    def reset_ui(self): # Define method to clear the UI
        self.typing_text_widget.config(state=tk.NORMAL) # Enable typing area to clear it
        self.typing_text_widget.delete("1.0", tk.END) # Clear all text in typing area
        self.typing_text_widget.config(state=tk.DISABLED) # Disable typing area until test starts
        self.time_lbl.config(text="⏱ Time: --s") # Reset time label
        self.wpm_lbl.config(text="🚀 WPM: --") # Reset WPM label
        self.acc_lbl.config(text="🎯 Accuracy: --%") # Reset accuracy label
        self.correct_lbl.config(text="✅ Correct: --") # Reset correct label
        self.update_target_display() # Update the target display with current text

    def start_test(self): # Define method triggered by Start Test button
        try: # Start try block for error handling
            self.current_text = TextBank.get_random() # Fetch a new random text from TextBank
            self.session = TypingSession(self.current_text) # Create a new TypingSession instance
            
            self.update_target_display() # Display the target text in the target widget
            
            self.typing_text_widget.config(state=tk.NORMAL) # Enable the typing area for the user
            self.typing_text_widget.delete("1.0", tk.END) # Clear any old text from typing area
            self.typing_text_widget.focus_set() # Focus the cursor on the typing area
            
            self.session.start() # Start the typing session to record time
            self.status_bar.config(text="⚡ Typing test in progress... Type as fast as you can!") # Update status bar
        except TypingException as e: # Catch custom TypingException errors
            tk.messagebox.showwarning("Typing Error", str(e)) # Show warning dialog for typing errors
        except Exception as e: # Catch all other exceptions
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {e}") # Show error dialog for general errors

    def stop_test(self): # Define method triggered by Stop & Results button
        try: # Start try block for error handling
            if not self.session or not self.session.is_active: # Check if session exists and is active
                raise TypingException("No active session to stop!") # Raise error if no active session
                
            self.session.stop() # Stop the session to record end time
            typed_text = self.typing_text_widget.get("1.0", "end-1c") # Retrieve all text typed by the user
            
            results = self.session.get_results(typed_text) # Get the calculated metrics from the session
            
            self.time_lbl.config(text=f"⏱ Time: {results['elapsed_time']}s") # Update the time label
            self.wpm_lbl.config(text=f"🚀 WPM: {results['wpm']}") # Update the WPM label
            self.acc_lbl.config(text=f"🎯 Accuracy: {results['accuracy']}%") # Update the accuracy label
            self.correct_lbl.config(text=f"✅ Correct: {results['correct_chars']}/{results['total_chars']}") # Update the correct characters label
            
            self.typing_text_widget.config(state=tk.DISABLED) # Disable the typing area to prevent further typing
            self.status_bar.config(text="✅ Test completed! Check your results or start a new text.") # Update status bar
            
            msg = f"Time: {results['elapsed_time']}s\nWPM: {results['wpm']}\nAccuracy: {results['accuracy']}%\nCorrect Chars: {results['correct_chars']}/{results['total_chars']}" # Format results message
            tk.messagebox.showinfo("Test Results", msg) # Show results in a popup messagebox
        except TypingException as e: # Catch custom TypingException errors
            tk.messagebox.showwarning("Session Error", str(e)) # Show warning dialog for session errors
        except Exception as e: # Catch all other exceptions
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {e}") # Show error dialog for general errors

    def new_text(self): # Define method triggered by New Text button
        try: # Start try block for error handling
            self.session = None # Clear the current session
            self.current_text = TextBank.get_random() # Get a brand new random text
            self.reset_ui() # Reset all UI elements
            self.status_bar.config(text="⌨️ Click 'Start Test' to begin...") # Reset status bar
        except Exception as e: # Catch any potential errors
            tk.messagebox.showerror("Error", f"Failed to load new text: {e}") # Show error dialog if loading fails

    def on_key_release(self, event): # Define method triggered by any key release in typing area
        try: # Start try block for error handling
            if not self.session or not self.session.is_active: # Check if there is an active session
                return # Exit method early if no active test
                
            typed_text = self.typing_text_widget.get("1.0", "end-1c") # Get current typed string without trailing newline
            target = self.session.target_text # Store local reference to target text
            
            self.typing_text_widget.tag_remove("correct", "1.0", tk.END) # Clear all 'correct' tags from text
            self.typing_text_widget.tag_remove("wrong", "1.0", tk.END) # Clear all 'wrong' tags from text
            
            for i in range(len(typed_text)): # Iterate through each character typed so far
                start_idx = f"1.0+{i}c" # Calculate the start Tkinter text index
                end_idx = f"1.0+{i+1}c" # Calculate the end Tkinter text index
                
                if i < len(target) and typed_text[i] == target[i]: # Check if character matches target
                    self.typing_text_widget.tag_add("correct", start_idx, end_idx) # Apply 'correct' tag (green)
                else: # Execute if character is incorrect or exceeds target length
                    self.typing_text_widget.tag_add("wrong", start_idx, end_idx) # Apply 'wrong' tag (red)
        except Exception as e: # Catch any exceptions during live highlighting
            pass # Silently ignore highlighting errors to avoid disrupting typing flow

if __name__ == "__main__": # Check if this script is being run directly
    root = tk.Tk() # Create the main Tk root window
    app = TypeBlastApp(root) # Instantiate the TypeBlastApp class
    root.mainloop() # Start the main Tkinter event loop
