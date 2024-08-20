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

PVmesh use primarly [GMSH](https://gmsh.info) as the backend for mesh generation and  [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/) for the GUI.

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

![alt text](figures/gui2.png "")

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

### Variables 

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
- file_format: format of the generated mesh



- parameters `a`,`b`,`c`,`h` are frame parameters and are shown in the frame illustration in the GUI picture above. 

- clip_thick: open space of frame ( `d`) 
- seal_length: width of seal (distance from panel edge to frame, `f`)
- frame_thick:  thickness of frame (`t`)





### Panel Geometry

Once the variables are defined, the panel geometry is created in steps. 
The panel is decomposed into 7 substructures: frame, back_sheet, back_encap, cell_layer, front_encap, front_glass and cells. 
to finalize the geometry a seal is added to close the gap between the frame and the multilayered panel. 

### Panel mesh 

The geometry created is sorted to obtain 1D, 2D and 3D elements. 
Each substructor is meshed based on its geometry.
Adaptive mesh refinement is used to reduce mesh density where its not needed. 









refrences 
