import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import subprocess
import os
import tempfile

# from tkHyperLinkManager import HyperlinkManager
# import webbrowser
# from functools import partial

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
    cell_width = cell_width_entry.get()
    cell_length = cell_length_entry.get()
    n_cell_length = n_cell_length_entry.get()
    n_cell_width = n_cell_width_entry.get()
    front_glass_thick = front_glass_thick_entry.get()
    front_encap_thick = front_encap_thick_entry.get()
    back_encap_thick = back_encap_thick_entry.get()
    back_sheet_thick = back_sheet_thick_entry.get()
    file_format = file_format_entry.get()

    # back_sheet_thick = back_sheet_thick_entry.get()
    perimeter_margin = perimeter_margin_entry.get()
    cell_cell_gap_x = cell_cell_gap_x_entry.get()
    cell_cell_gap_y = cell_cell_gap_y_entry.get()
    clip_thick = clip_thick_entry.get()
    seal_length = seal_length_entry.get()
    frame_thick = frame_thick_entry.get()


    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Generate a random filename for the text file
    random_filename = "input" #next(tempfile._get_candidate_names())
    text_file_path = os.path.join(script_directory, random_filename + ".txt")

    # Write input values to the text file
    with open(text_file_path, 'w') as file:
        file.write(f"cell_thick: {cell_thick}\n")
        file.write(f"cell_width: {cell_width}\n")
        file.write(f"cell_length: {cell_length}\n")
        file.write(f"n_cell_length: {n_cell_length}\n")
        file.write(f"n_cell_width: {n_cell_width}\n")
        file.write(f"front_glass_thick: {front_glass_thick}\n")
        file.write(f"front_encap_thick: {front_encap_thick}\n")
        file.write(f"back_encap_thick: {back_encap_thick}\n")
        file.write(f"back_sheet_thick: {back_sheet_thick}\n")
        file.write(f"file_format: {file_format}\n")

        # file.write(f"back_sheet_thick: {file_format}\n")
        file.write(f"perimeter_margin: {perimeter_margin}\n")
        file.write(f"cell_cell_gap_x: {cell_cell_gap_x}\n")
        file.write(f"cell_cell_gap_y: {cell_cell_gap_y}\n")
        file.write(f"clip_thick: {clip_thick}\n")
        file.write(f"seal_length: {seal_length}\n")
        file.write(f"frame_thick: {frame_thick}\n")

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
            output_text = output_text[-500000:]  # Limiting the output to 500 characters
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
PVmesh is an opensource software that generate a mesh for photovoltaic panels in multiple formats.
 The geometry of the PV panel can be mofified through a set of variables. 
 PVmesh can be used through a graphical user interface (GUI) or by modifying a yaml input file.
 The GUI has preset values for all variables that control the geometry of the panel.
"""
intro_label = tk.Label(root, text=intro_text)
intro_label.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="w")

# Load preset values from a different text file
preset_file_path = "original.txt"  # Replace with the actual path of the preset file
preset_values = load_preset_values(preset_file_path)


row_index = 1 
# Display preset values
preset_label_text = "Preset Values:"
preset_label = tk.Label(root, text=preset_label_text, font=("Arial", 10, "bold"))
preset_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
row_index += 1


def create_label_entry (row_index, name_of_var, name_of_cell, root , preset_values):
    var_label = tk.Label(root, text=name_of_cell)
    var_label.grid(row=row_index, column=0, padx=5, pady=5, sticky="e")
    var_entry = tk.Entry(root)
    var_entry.insert(0, preset_values.get(name_of_var, ""))
    var_entry.grid(row=row_index, column=1, padx=5, pady=5)
    row_index +=1
    return var_label , var_entry, row_index

cell_thick_label, cell_thick_entry, row_index = create_label_entry (row_index, "cell_thick","Cell thickness (mm)", root , preset_values)
cell_width_label, cell_width_entry, row_index = create_label_entry (row_index, "cell_width","Cell width (mm)", root , preset_values)
cell_length_label, cell_length_entry, row_index = create_label_entry (row_index, "cell_length", "Cell length (mm)",root , preset_values)
n_cell_length_label, n_cell_length_entry, row_index = create_label_entry (row_index, "n_cell_length", "Number of cells lengthwise", root , preset_values)
n_cell_width_label, n_cell_width_entry, row_index = create_label_entry (row_index, "n_cell_width", "Number of cells in the width direction", root , preset_values)
cell_cell_gap_x_label, cell_cell_gap_x_entry, row_index = create_label_entry (row_index, "cell_cell_gap_x", "Gap between cell along x (mm)", root , preset_values)
cell_cell_gap_y_label, cell_cell_gap_y_entry, row_index = create_label_entry (row_index, "cell_cell_gap_y", "Gap between cell along y (mm)", root , preset_values)
perimeter_margin_label, perimeter_margin_entry, row_index = create_label_entry (row_index, "perimeter_margin", "Edge margin (mm)", root , preset_values)
clip_thick_label, clip_thick_entry, row_index = create_label_entry (row_index, "clip_thick", "Open space of frame (mm)", root , preset_values)
seal_length_label, seal_length_entry, row_index = create_label_entry (row_index, "seal_length", "Width of seal  ?? (mm)", root , preset_values)
frame_thick_label, frame_thick_entry, row_index = create_label_entry (row_index, "frame_thick", "Thickness of the frame (mm)", root , preset_values)
front_glass_thick_label, front_glass_thick_entry, row_index = create_label_entry (row_index, "front_glass_thick", "Thickness of the front glass (mm)", root , preset_values)
front_encap_thick_label, front_encap_thick_entry, row_index = create_label_entry (row_index, "front_encap_thick", "Thickness of the front encapsulent (mm)", root , preset_values)
back_encap_thick_label, back_encap_thick_entry, row_index = create_label_entry (row_index, "back_encap_thick", "Thickness of the back encapsulent (mm)", root , preset_values)
back_sheet_thick_label, back_sheet_thick_entry, row_index = create_label_entry (row_index, "back_sheet_thick", "Thickness of the back sheet (mm)", root , preset_values)
file_format_label, file_format_entry, row_index = create_label_entry (row_index, "file_format", "Mesh file format",root , preset_values)



# Load an image
img = tk.PhotoImage(file="pv_model.png")  # Replace "image.png" with the path to your image

# Display the image
img_label = tk.Label(root, image=img)
img_label.grid(row=2, column=2, rowspan=6, padx=10, pady=10, sticky="w")

# Output text widget to display subprocess output
output_text_widget = scrolledtext.ScrolledText(root, width=60, height=50)
output_text_widget.grid(row=2, column=3, rowspan=6, padx=10, pady=10, sticky="w")

# Footnote
footnote_text = "For more information please visit https://github.com/NREL/PVMesh."

# footnote_text = "TutorialsPoint",hyperlink.add(partial(webbrowser.open,"http://www.tutorialspoint.com"))


footnote_label = tk.Label(root, text=footnote_text, font=("Arial", 8), fg="gray")
footnote_label.grid(row=row_index, column=0, columnspan=2, padx=10, pady=5, sticky="w")
row_index +=1

# Button to generate text file and execute script
execute_button = tk.Button(root, text="Generate Input File and Create the Mesh", command=generate_text_and_execute_script)
execute_button.grid(row=row_index, columnspan=2, padx=5, pady=10)
row_index +=1
# Label to display result
result_label = tk.Label(root, text="")
result_label.grid(row=row_index, columnspan=2)

# Start GUI main loop
root.mainloop()
