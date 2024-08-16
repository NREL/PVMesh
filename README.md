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

PVmesh use primarly gmsh as the backend for mesh generation and tkinter for the GUI.

Installation of the pre-requisits for PVmesh can be done through conda/mamba using the follwing command



Executing PVmesh can be done through 
1- python gui.py 

or 

2- python mesh_manager.py --input input.yaml 











refrences 
