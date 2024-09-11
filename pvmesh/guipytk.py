import itertools
import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea, QFormLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QProcess,QEventLoop
# from PyQt5.QtCore import QProcess, QCoreApplication, QEventLoop
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.on_process_finished)

        self.initUI()

    def initUI(self):
        def resource_path(relative_path):
            """Get the absolute path to a resource, works for dev and for PyInstaller"""
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        # Layouts
        mainLayout = QHBoxLayout()

        # Center side: Images
        self.imageLabel1 = QLabel()
        self.imageLabel2 = QLabel()

        # Load and resize images
        pixmap1 = QPixmap(resource_path('figures/pv_model.png'))
        pixmap2 = QPixmap(resource_path('figures/frame3.png'))
        resized_pixmap1 = pixmap1.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)
        resized_pixmap2 = pixmap2.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio)

        self.imageLabel1.setPixmap(resized_pixmap1)
        self.imageLabel2.setPixmap(resized_pixmap2)

        centerLayout = QVBoxLayout()
        centerLayout.addWidget(self.imageLabel1)
        centerLayout.addWidget(self.imageLabel2)

        # Scroll Area for right side
        scrollArea = QScrollArea()
        scrollWidget = QWidget()
        rightLayout = QVBoxLayout()

        # Right side: Variables and input fields
        self.inputFields = {}
        variable_names = [
            'cell_thick', 'cell_width', 'cell_length', 'n_cell_length', 'n_cell_width',
            'front_glass_thick', 'front_encap_thick', 'back_encap_thick', 'file_format',
            'back_sheet_thick', 'perimeter_margin', 'cell_cell_gap_x', 'cell_cell_gap_y',
            'clip_thick', 'seal_length', 'frame_thick', 'c', 'b', 'a', 'h',
            'mesh_size_in_cell', 'mesh_size_out_cell', 'mounting_area_shape', 'mounting_area_size', 'mounting_location'
        ]

        # Create input fields
        formLayout = QFormLayout()
        for var in variable_names:
            inputField = QLineEdit()
            inputField.textChanged.connect(self.validateInput)
            self.inputFields[var] = inputField
            formLayout.addRow(QLabel(var), inputField)

        rightLayout.addLayout(formLayout)

        # Button to generate input files for combinations
        self.generateFilesButton = QPushButton("Generate Input Files")
        self.generateFilesButton.clicked.connect(self.generateInputFiles)
        rightLayout.addWidget(self.generateFilesButton)

        # Button to execute Python file
        self.executeButton = QPushButton("Generate mesh")
        self.executeButton.clicked.connect(self.executeScript)
        rightLayout.addWidget(self.executeButton)


        # Text area for output
        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        rightLayout.addWidget(self.outputText)

        scrollWidget.setLayout(rightLayout)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)

        # Add image layout and scroll area to main layout
        mainLayout.addLayout(centerLayout)
        mainLayout.addWidget(scrollArea)

        self.setLayout(mainLayout)
        self.setWindowTitle('PV panels generator (PVmesh)')
        self.setGeometry(100, 100, 1200, 1000)

        # Set preset values
        self.setPresetValues(variable_names)

    def setPresetValues(self, variable_names):
        def resource_path(relative_path):
            """Get the absolute path to a resource, works for dev and for PyInstaller"""
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        try:
            with open(resource_path('original.txt'), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if ':' in line:
                        var, value = line.split(':', 1)
                        var = var.strip()
                        value = value.strip()
                        if var in self.inputFields:
                            self.inputFields[var].setText(value)
        except FileNotFoundError:
            self.outputText.append("Error: 'original.txt' file not found.")
        except Exception as e:
            self.outputText.append(f"An error occurred: {e}")

    def validateInput(self):
        for var, field in self.inputFields.items():
            text = field.text()
            if var in ['cell_thick', 'cell_width', 'cell_length', 'n_cell_length', 'n_cell_width', 'front_glass_thick',
                       'front_encap_thick', 'back_encap_thick', 'back_sheet_thick', 'perimeter_margin', 'cell_cell_gap_x',
                       'cell_cell_gap_y', 'clip_thick', 'seal_length', 'frame_thick', 'c', 'b', 'a', 'h', 'mesh_size_in_cell',
                       'mesh_size_out_cell', 'mounting_area_size', 'mounting_location']:
                if not text.replace('.', '', 1).isdigit():
                    field.setStyleSheet("border: 1px solid red;")
                else:
                    field.setStyleSheet("border: 1px solid green;")

    def executeScript(self):
        def resource_path(relative_path):
            """Get the absolute path to a resource, works for dev and for PyInstaller"""
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        # # Collect input values
        # inputValues = {key: field.text() for key, field in self.inputFields.items()}

        # # Save input values to 'input.txt'
        # try:
        #     with open(resource_path('input.txt'), 'w') as file:
        #         for key, value in inputValues.items():
        #             file.write(f"{key}: {value}\n")
        # except IOError as e:
        #     self.outputText.clear()
        #     self.outputText.append(f"Error saving to 'input.txt': {e}")
        #     return


        script_path = resource_path('pvmesh/mesh_generator.py')

        directory = os.getcwd()
        prefix = "input"
        for entry in os.listdir(directory):
            # Construct the full path
            full_path = os.path.join(directory, entry)

            # Check if the entry is a directory and starts with the prefix
            if os.path.isdir(full_path) and entry.startswith(prefix):
                print(f"Found directory: {full_path}")
                for filename in os.listdir(full_path):
                    file_path = os.path.join(full_path, filename)
                    print("generating mesh for ", filename)
                    command = ['python3', script_path, file_path, os.path.basename(full_path)]
                    self.process.start(command[0], command[1:])
                    # Create an event loop to wait for the process to finish
                    loop = QEventLoop()
                    self.process.finished.connect(loop.quit)
                    loop.exec_()  # Start the event loop and wait for the process to finish


        # for filename in os.listdir(resource_path('combinations')):
        #     # Construct the full file path
        #     file_path = os.path.join(resource_path('combinations'), filename)
        #     print("generating mesh for ", filename)
        #     command = ['mpirun', '-n', '1', 'python', script_path, file_path, filename]
        #     self.process.start(command[0], command[1:])

    def generateInputFiles(self):
        self.outputText.clear()
        def resource_path(relative_path):
            """Get the absolute path to a resource, works for dev and for PyInstaller"""
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        try:
            # Extract values from input fields
            values = {}
            for var in self.inputFields:
                text = self.inputFields[var].text()
                if text:
                    values[var] = text.split(',')  # Split by comma to get different values

            # Generate all combinations
            all_combinations = list(itertools.product(*values.values()))


            for i, combo in enumerate(all_combinations):
                # Write each combination to a separate file
                output_dir = resource_path(f'input{i + 1}')
                os.makedirs(output_dir, exist_ok=False)
                combo_dict = dict(zip(values.keys(), combo))
                file_path = os.path.join(output_dir, f'input_{i + 1}.txt')
                with open(file_path, 'w') as file:
                    for key, value in combo_dict.items():
                        file.write(f"{key}: {value}\n")

            self.outputText.append(f"Generated {len(all_combinations)} files in '{output_dir}'")

        except Exception as e:
            self.outputText.append(f"An error occurred while generating input files: {e}")

        # # Prepare command to execute your Python script
        # script_path = resource_path('pvmesh/mesh_generator.py')
        # for filename in os.listdir(resource_path('combinations')):
        #     # Construct the full file path
        #     file_path = os.path.join(resource_path('combinations'), filename)
        #     command = ['mpirun', '-n', '1', 'python', script_path, file_path]
        #     self.process.start(command[0], command[1:])




    def handle_stdout(self):
        # Append standard output to the output text box
        data = self.process.readAllStandardOutput().data().decode()
        self.outputText.append(data)
        self.outputText.verticalScrollBar().setValue(self.outputText.verticalScrollBar().maximum())

    def handle_stderr(self):
        # Append standard error to the output text box
        data = self.process.readAllStandardError().data().decode()
        self.outputText.append(f"Error: {data}")
        self.outputText.verticalScrollBar().setValue(self.outputText.verticalScrollBar().maximum())

    def on_process_finished(self):
        # Process finished, handle any final updates if needed
        self.outputText.append("Process finished.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec_())
