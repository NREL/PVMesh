# PVMesh


PVmesh is an opensource software that generate a mesh for photovoltaic panels in multiple formats. 
The geometry of the PV panel can be mofified through a set of variables.
PVmesh can be used through a graphical user interface (GUI) or by modifying a yaml input file.
The GUI has preset values for all variables that control the geometry of the panel. 
Among the file formats that can be generated with PVmesh we have:
- `.msh` for ANSYS 
- `.bdf` for COMSOL 
- `.vtk`for FEnics/FEniCSx 
- `.inp`for ABAQUS 


## Getting Started 

PVmesh use primarly gmsh as the backend for mesh generation and tkinter/pyQt for the GUI.

Installation of the pre-requisits for PVmesh can be done through conda/mamba using the follwing command

```
mamba env create -n pvmesh -f environment.yaml
```

The environement created can be activated using the command 

``` 
mamba activate pvmesh
```

### PVmesh example

Executing PVmesh can be done through the GUI or using CLI. 
The GUI can be executed by executing

```
python guipytk.py.py 
```

The GUI should appear as a pop-up window. 

![alt text](GUI2.png "")

The user interface should look like this. 
The two figures demonstrate what the variables controls. 
All variables are preset using the file original.txt.
They can also be modified to obtain the a mesh that meets your dimensions. 
Once the variables are set, you can press the execution button which will write all variables to a new file `input.txt` and execute mesh_generator.py.
The mesh generated will be under the name `panel_geo` with the extension specified in the GUI. 
The available file formats are:
 - `.msh` for ANSYS
 - `.bdf` for COMSOL
 - `.vtk`for FEnics/FEniCSx
 - `.inp`for ABAQUS



PVmesh can also be used through CLI. 
A file containing all variables and their assigned values needs to be created under the name `input.txl`.
This file needs to follow the same structure as `original.txt`. 
The mesh generator can then be executed using 

```
python mesh_generator.py
```



mesh_generator.py is the file that creates the geometry and mesh using GMSH. 
It reads all variables from input.txt (created by the GUI).  
In the case where input.txt is not available, mesh_generator.py will use original.txt to set the variables.



## Code structure:  mesh_generator.py


The variables that control the geometry of the panel are the following:

- cell_thick: thickness of cell 
  
- cell_width: width of each cell 
- cell_length: length of each cell 
- n_cell_length: number of cells along x       
- n_cell_width: number of cells along y   
- cell_cell_gap_x: gap between cell along x
- cell_cell_gap_y: gap between cell along y

- front_glass_thick: thickness of gront glass layer
- front_encap_thick: thickness of front encapsulant layer
- back_encap_thick: thickness of back encapsulant layer

- back_sheet_thick: thickness of backsheet or back glass
- perimeter_margin: edge margin

- clip_thick: open space of frame (parameter d)
- seal_length: width of seal (distance from panel edge to frame, parameter f)
- frame_thick:  thickness of frame (paramater t)
- c: 12.0
- b: 4.0
- a: 35.0
- h: 50.0

file_format: format of the generated mesh












refrences 
