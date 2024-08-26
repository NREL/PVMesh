import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea, QFormLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os 
from PyQt5.QtCore import QProcess

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
            """ Get the absolute path to a resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temporary folder and stores the path in _MEIPASS
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
        # pixmap1 = QPixmap(PVmesh_dir+'/pv_model.png')
        # pixmap2 = QPixmap(PVmesh_dir+'/frame3.png')
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
            'mesh_size_in_cell','mesh_size_out_cell','mounting_area_shape','mounting_area_size','mounting_location'
        ]
        
        # Create input fields
        print("Initializing input fields...")  # Debug statement
        formLayout = QFormLayout()  # Use QFormLayout for better alignment of labels and input fields
        for var in variable_names:
            inputField = QLineEdit()
            inputField.textChanged.connect(self.validateInput)  # Connect input change event to validation
            self.inputFields[var] = inputField
            formLayout.addRow(QLabel(var), inputField)
            print(f"Added {var} to inputFields.")  # Debug statement
        
        rightLayout.addLayout(formLayout)
        
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
        self.setGeometry(100, 100, 1200, 800)  # Adjust window size as needed
        
        # Set preset values
        self.setPresetValues(variable_names)

    def setPresetValues(self, variable_names):
        def resource_path(relative_path):
            """ Get the absolute path to a resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temporary folder and stores the path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)
        
        print("Setting preset values...")  # Debug statement
        try:
            with open(resource_path('original.txt'), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if ':' in line:
                        var, value = line.split(':', 1)
                        var = var.strip()
                        value = value.strip()
                        if var in self.inputFields:
                            print(f"Setting {var} to {value}")  # Debug statement
                            self.inputFields[var].setText(value)
                        else:
                            print(f"Variable {var} not found in inputFields")  # Debug statement
        except FileNotFoundError:
            print("Error: 'original.txt' file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def validateInput(self):
        for var, field in self.inputFields.items():
            text = field.text()
            if var in ['cell_thick', 'cell_width', 'cell_length',\
                        'n_cell_length', 'n_cell_width', 'front_glass_thick',\
                              'front_encap_thick', 'back_encap_thick', 'back_sheet_thick',\
                                  'perimeter_margin', 'cell_cell_gap_x', 'cell_cell_gap_y',\
                                      'clip_thick', 'seal_length', 'frame_thick',\
                                          'c', 'b', 'a', 'h','mesh_size_in_cell',\
                                            'mesh_size_out_cell','mounting_area_size','mounting_location']:
                if not text.replace('.', '', 1).isdigit():
                    field.setStyleSheet("border: 1px solid red;")
                else:
                    field.setStyleSheet("border: 1px solid green;")

    def executeScript(self):
        def resource_path(relative_path):
            """ Get the absolute path to a resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temporary folder and stores the path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)
        # PVmesh_dir = os.getcwd()
        # Collect input values
        inputValues = {key: field.text() for key, field in self.inputFields.items()}
        
        # Save input values to 'input.txt'
        try:
            with open(resource_path('input.txt'), 'w') as file:
                for key, value in inputValues.items():
                    file.write(f"{key}: {value}\n")
            print("Input values saved to 'input.txt'.")  # Debug statement
        except IOError as e:
            self.outputText.clear()
            self.outputText.append(f"Error saving to 'input.txt': {e}")
            return

        # Prepare command to execute your Python script
        script_path = resource_path('pvmesh/mesh_generator.py')

        print('script_path')


        command = ['python', script_path]

        self.process.start('mpirun', ['-n', str(1), 'python', script_path])

        # # Use a try-except block to handle exceptions during script execution
        # try:
        #     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #     stdout, stderr = process.communicate()

        #     # Update output text area
        #     self.outputText.clear()
        #     if stdout:
        #         self.outputText.append("Output:\n" + stdout)
        #     if stderr:
        #         self.outputText.append("Errors:\n" + stderr)
            
        #     if process.returncode != 0:
        #         # If the script returns a non-zero exit code, display a general error message
        #         self.outputText.append(f"Script execution failed with exit code {process.returncode}.")
        
        # except FileNotFoundError:
        #     self.outputText.clear()
        #     self.outputText.append(f"Error: The script file '{script_path}' was not found.")
        # except Exception as e:
        #     self.outputText.clear()
        #     self.outputText.append(f"An unexpected error occurred: {e}")


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

