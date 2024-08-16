import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import subprocess
import os
import tempfile

def load_preset_values(preset_file_path):
    # Initialize variables
    preset_values = {}

    # Read preset values from the text file
    with open(preset_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split(": ")
            preset_values[key] = value

    return preset_values

def generate_text_and_execute_script():
    # Retrieve input values
    cell_thick = cell_thick_entry.get()
    n_cell_length = n_cell_length_entry.get()
    n_cell_width = n_cell_width_entry.get()
    front_glass_thick = var1_entry.get()
    front_encap_thick = var2_entry.get()
    back_encap_thick = var3_entry.get()
    
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Generate a random filename for the text file
    random_filename = "input" #next(tempfile._get_candidate_names())
    text_file_path = os.path.join(script_directory, random_filename + ".txt")
    
    # Write input values to the text file
    with open(text_file_path, 'w') as file:
        file.write(f"cell_thick: {cell_thick}\n")
        file.write(f"n_cell_length: {n_cell_length}\n")
        file.write(f"n_cell_width: {n_cell_width}\n")
        file.write(f"front_glass_thick: {front_glass_thick}\n")
        file.write(f"front_encap_thick: {front_encap_thick}\n")
        file.write(f"back_encap_thick: {back_encap_thick}\n")
        
    # Inform the user that the text file has been generated
    result_label.config(text="Text file generated successfully!")
    
    # Execute the other Python script with the input values as arguments
    script_path = "mesh_generator.py"
    command = ["python", script_path, cell_thick, n_cell_length, n_cell_width, front_glass_thick, front_encap_thick, back_encap_thick]
    
    # Start the subprocess and capture its output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    # Display the output in the result text widget
    output_text = ""
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() is not None:
            break
        if line:
            output_text += line.strip() + "\n"
            output_text = output_text[-500:]  # Limiting the output to 500 characters
            output_text_widget.config(state=tk.NORMAL)
            output_text_widget.delete(1.0, tk.END)  # Clear previous output
            output_text_widget.insert(tk.END, output_text)
            output_text_widget.config(state=tk.DISABLED)  # Prevent editing of output
            output_text_widget.see(tk.END)  # Scroll to the bottom
    
    # Wait for the subprocess to finish
    process.wait()
    
    # Inform the user that the script has been executed
    result_label.config(text=result_label.cget("text") + "\nScript executed successfully!")

# Create GUI window
root = tk.Tk()
root.title("PV panels generator (PVmesh)")

# Paragraph at the top
intro_text = """
Welcome to the Text File Generator and Script Executor.
Please fill out the following information:
"""
intro_label = tk.Label(root, text=intro_text)
intro_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Load preset values from a different text file
preset_file_path = "original.txt"  # Replace with the actual path of the preset file
preset_values = load_preset_values(preset_file_path)

# Display preset values
preset_label_text = "Preset Values:"
preset_label = tk.Label(root, text=preset_label_text, font=("Arial", 10, "bold"))
preset_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# cell_thick input with preset value
cell_thick_label = tk.Label(root, text="cell_thick:")
cell_thick_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
cell_thick_entry = tk.Entry(root)
cell_thick_entry.insert(0, preset_values.get("cell_thick", ""))
cell_thick_entry.grid(row=2, column=1, padx=5, pady=5)

# n_cell_length input with preset value
n_cell_length_label = tk.Label(root, text="n_cell_length:")
n_cell_length_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
n_cell_length_entry = tk.Entry(root)
n_cell_length_entry.insert(0, preset_values.get("n_cell_length", ""))
n_cell_length_entry.grid(row=3, column=1, padx=5, pady=5)

# n_cell_width input with preset value
n_cell_width_label = tk.Label(root, text="n_cell_width:")
n_cell_width_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
n_cell_width_entry = tk.Entry(root)
n_cell_width_entry.insert(0, preset_values.get("n_cell_width", ""))
n_cell_width_entry.grid(row=4, column=1, padx=5, pady=5)

# Additional front_glass_thick input with preset value
var1_label = tk.Label(root, text="front_glass_thick:")
var1_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
var1_entry = tk.Entry(root)
var1_entry.insert(0, preset_values.get("front_glass_thick", ""))
var1_entry.grid(row=5, column=1, padx=5, pady=5)

# Additional front_encap_thick input with preset value
var2_label = tk.Label(root, text="front_encap_thick:")
var2_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
var2_entry = tk.Entry(root)
var2_entry.insert(0, preset_values.get("front_encap_thick", ""))
var2_entry.grid(row=6, column=1, padx=5, pady=5)

# Additional back_encap_thick input with preset value
var3_label = tk.Label(root, text="back_encap_thick:")
var3_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
var3_entry = tk.Entry(root)
var3_entry.insert(0, preset_values.get("back_encap_thick", ""))
var3_entry.grid(row=7, column=1, padx=5, pady=5)

# Load an image
img = tk.PhotoImage(file="panel.png")  # Replace "image.png" with the path to your image

# Display the image
img_label = tk.Label(root, image=img)
img_label.grid(row=2, column=2, rowspan=6, padx=10, pady=10, sticky="w")

# Output text widget to display subprocess output
output_text_widget = scrolledtext.ScrolledText(root, width=40, height=10)
output_text_widget.grid(row=2, column=3, rowspan=6, padx=10, pady=10, sticky="w")

# Footnote
footnote_text = "This is a footnote."
footnote_label = tk.Label(root, text=footnote_text, font=("Arial", 8), fg="gray")
footnote_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Button to generate text file and execute script
execute_button = tk.Button(root, text="Generate Text File and Execute Script", command=generate_text_and_execute_script)
execute_button.grid(row=9, columnspan=2, padx=5, pady=10)

# Label to display result
result_label = tk.Label(root, text="")
result_label.grid(row=10, columnspan=2)

# Start GUI main loop
root.mainloop()
