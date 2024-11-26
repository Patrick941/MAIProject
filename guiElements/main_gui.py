import ctypes
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import os
import subprocess
import sys

def create_gui():
    # Set DPI Awareness
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    # Initialize root window
    root = ttk.Window(themename="darkly")
    root.title("Debugging Problems")
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

    # Create and apply a ttk.Style for consistent sizing
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", new_font_size))
    style.configure("TButton", font=("Helvetica", new_font_size), padding=(10, 10))  # Add more padding to buttons

    def browse_directory():
        # Set initial directory dialog size by defining options
        directory = filedialog.askdirectory(title="Select Directory", initialdir="/")
        if directory:
            results_directory_entry.delete(0, 'end')
            results_directory_entry.insert(0, directory)

    def submit():
        type_value = type_entry.get()
        amount_value = int(amount_entry.get())
        save_scripts_value = save_scripts_var.get()
        model_value = model_entry.get()
        results_directory_value = results_directory_entry.get()
        prompt_override_value = prompt_override_entry.get()
        bug_override_value = bug_override_entry.get()

        # Handle form values
        print(f"type: {type_value}, amount: {amount_value}, save_scripts: {save_scripts_value}, "
            f"model: {model_value}, results_directory: {results_directory_value}, "
            f"prompt_override: {prompt_override_value}, bug_override: {bug_override_value}")
        
        # Construct the command to run main.py with the collected arguments
        if bug_override_entry == "" or bug_override_entry == "None":
            command = [
                sys.executable,  # Use the current Python interpreter
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py"),
                "--type", type_value,
                "--amount", str(amount_value),
                "--save-scripts", str(save_scripts_value),
                "--model", model_value,
                "--results-directory", results_directory_value
            ] 
        else:
            command = [
                sys.executable,  # Use the current Python interpreter
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py"),
                "--type", type_value,
                "--amount", str(amount_value),
                "--save-scripts", str(save_scripts_value),
                "--model", model_value,
                "--results-directory", results_directory_value,
                "--prompt-override", prompt_override_value,
                "--bug-override", bug_override_value
            ]          
        
        # Run the command
        subprocess.Popen(command)
        
        # Destroy the window to end mainloop
        root.destroy()

    # Add form fields with updated layout
    title_font = ("Helvetica", new_font_size + 4, "bold")  # Increase font size and make it bold

    ttk.Label(root, text="Type:", bootstyle="secondary", font=title_font).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    type_entry = ttk.Entry(root, bootstyle="success")
    type_entry.insert(0, "ollama")  # Set default value
    type_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(root, text="Amount:", bootstyle="secondary", font=title_font).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    amount_entry = ttk.Entry(root, bootstyle="success")
    amount_entry.insert(0, "10")  # Set default value
    amount_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(root, text="Save Scripts:", bootstyle="secondary", font=title_font).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    save_scripts_var = ttk.BooleanVar(value=True)  # Set default value
    save_scripts_check = ttk.Checkbutton(root, variable=save_scripts_var, bootstyle="round-toggle")
    save_scripts_check.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="Model:", bootstyle="secondary", font=title_font).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    model_entry = ttk.Entry(root, bootstyle="success")
    model_entry.insert(0, "mistral-small")  # Set default value
    model_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(root, text="Results Directory:", bootstyle="secondary", font=title_font).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    results_directory_entry = ttk.Entry(root, bootstyle="success")
    current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_directory = os.path.join(current_directory, "artifacts")
    results_directory_entry.insert(0, default_directory)  # Set default value
    results_directory_entry.grid(row=4, column=1, sticky="ew", padx=(10, 5))
    browse_button = ttk.Button(root, text="Browse", command=browse_directory, bootstyle="info")
    browse_button.grid(row=4, column=2, padx=(5, 10), pady=5)

    ttk.Label(root, text="Prompt Override:", bootstyle="secondary", font=title_font).grid(row=5, column=0, sticky="w", padx=10, pady=5)
    prompt_override_entry = ttk.Entry(root, bootstyle="success")
    prompt_override_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(root, text="Bug Override:", bootstyle="secondary", font=title_font).grid(row=6, column=0, sticky="w", padx=10, pady=5)
    bug_override_entry = ttk.Entry(root, bootstyle="success")
    bug_override_entry.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

    # Add Submit button with modern styling
    submit_button = ttk.Button(root, text="Submit", command=submit, bootstyle="primary outline")
    submit_button.grid(row=7, column=0, columnspan=3, pady=20)

    # Make rows and columns responsive
    for i in range(8):
        root.rowconfigure(i, weight=1)
    root.columnconfigure(1, weight=1)

    # Initialize the font size and scaling once the window is ready
    root.after(100, update_scaling)

    root.mainloop()