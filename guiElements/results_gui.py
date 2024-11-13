import ctypes
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, Tk
import os

def display_results_gui():
    # Set DPI Awareness
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Makes the app DPI-aware
    except Exception:
        pass  # Ignore on unsupported systems

    # Initialize root window
    root = ttk.Window(themename="darkly")
    root.title("Debugging Problems Results")
    root.geometry("1920x1080")  # Use the new window size

    # Set global scaling factor (Increase to better handle high-DPI displays)
    root.tk.call("tk", "scaling", 1)  # Use a higher scaling factor for larger screens

    # Make the GUI responsive
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    # Get DPI setting for scaling
    dpi = root.winfo_fpixels('1i')  # Get DPI setting for scaling
    # Calculate new font size based on DPI
    new_font_size = int(dpi / 10)  # Adjust the formula to make text larger for bigger screens
    font = ("Helvetica", new_font_size)

    # Define the scaling behavior
    def update_scaling(event=None):
        # Calculate new font size based on window width
        new_font_size = max(14, int(root.winfo_width() / 60))  # Larger font size for big windows
        button_width = max(12, int(root.winfo_width() / 150))  # Button width based on window size
        button_padding = max(10, int(root.winfo_width() / 100))
        
        # Update font for all widgets
        font = ("Helvetica", new_font_size)
        for widget in root.winfo_children():
            try:
                widget.configure(font=font)
                if isinstance(widget, ttk.Button):
                    widget.configure(width=button_width, padding=button_padding)  # Increase width and padding for buttons
            except Exception:
                pass  # Ignore widgets that don't support font configuration

    # Bind the resize event to the update_scaling function
    root.bind("<Configure>", update_scaling)

    # Create and apply a ttk.Style for consistent sizing and appearance
    style = ttk.Style()
    style.configure("TLabel", 
                   font=("Helvetica", new_font_size), 
                   background='#2b2b2b',  # Dark grey background
                   foreground='white')     # White text
    style.configure("TButton", 
                   font=("Helvetica", new_font_size), 
                   padding=(10, 10))

    # Configure the root window background
    root.configure(background='#2b2b2b')  # Dark grey background

    # Temporary results dictionary
    results_dict = {
        "Problem Number": [3],
        "Cognitive Complexity": [15],
        "Cyclomatic Complexity": [9],
        "Attempts needed for original code": [6],
        "Attempts needed for bug insertion": [5],
        "Similarity": [0.95]
    }

    # Create a frame for the results with dark background
    results_frame = ttk.Frame(root, padding="10", style="Dark.TFrame")
    results_frame.grid(row=0, column=0, sticky=(N, S, E, W))

    # Configure dark frame style
    style.configure("Dark.TFrame", 
                   background='#2b2b2b')  # Dark grey background

    # Add labels and values to the frame in a table format
    for i, (key, value) in enumerate(results_dict.items()):
        label = ttk.Label(results_frame, text=key, style="TLabel")
        label.grid(row=i, column=0, sticky=W, padx=5, pady=5)
        value_label = ttk.Label(results_frame, text=str(value[0]), style="TLabel")
        value_label.grid(row=i, column=1, sticky=E, padx=5, pady=5)

    # Add a Submit button with the same styling as in the second example
    exit_button = ttk.Button(root, text="Exit", bootstyle="primary outline", command=root.quit)
    exit_button.grid(row=1, column=0, columnspan=2, pady=20)

    # Make rows and columns responsive
    for i in range(2):
        root.rowconfigure(i, weight=1)
    root.columnconfigure(1, weight=1)

    # Initialize the font size and scaling once the window is ready
    root.after(100, update_scaling)
    root.mainloop()