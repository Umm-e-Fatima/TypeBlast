import tkinter as tk # Import the core tkinter library to build the graphical user interface
import tkinter.messagebox # Import the messagebox module to display alert dialogs to the user
from gui import TypeBlastApp # Import the TypeBlastApp class from our local gui.py module file

if __name__ == "__main__": # Verify if the Python interpreter is running this script as the main program
    try: # Begin a try block to gracefully handle any unexpected crashes during the app startup phase
        root = tk.Tk() # Instantiate the foundational Tk application window and assign it to the root variable
        app = TypeBlastApp(root) # Create a new instance of our TypeBlastApp by passing the root window object
        root.mainloop() # Execute the main Tkinter event loop to render the UI and wait for user actions
    except Exception as e: # Intercept any generalized exceptions or errors that occur within the try block
        error_msg = f"Application failed to initialize: {e}" # Construct a detailed string containing the exact exception text
        tk.messagebox.showerror("Critical Error", error_msg) # Pop up a critical error dialog showing the failure message
