import numpy as np
import gmsh
import math


"""
code to generate PV panel geometry and mesh
"""


##################################
# define parameters
##################################

cell_length = 182.0/1000      # length of each cell in m
cell_width = 182.0/1000       # width of each cell in m
cell_thick = 0.17/1000   # thick ness of cell in m

n_cell_length = 3       # number of cells along x
n_cell_width = 2         # number of cells along y

perimeter_margin = 10.0/1000  # edge margin in m

cell_cell_gap_x = 2.5/1000  # gap between cell along x, in m
cell_cell_gap_y = 2.5/1000  # gap between cell along y, in m

front_glass_thick = 3.2/1000  # thickness of gront glass layer
front_encap_thick = 0.45/1000    # thickness of front encapsulant layer, in m
back_encap_thick = 0.45/1000     # thickness of back encapsulant layer, in m
back_sheet_thick = 0.35/1000     # thickness of backsheet or back glass, in m

panel_thick = cell_thick+front_glass_thick+front_encap_thick+back_encap_thick+back_sheet_thick
panel_length = cell_length*n_cell_length+(n_cell_length-1)*cell_cell_gap_x+2*perimeter_margin    # total length of the panel
panel_width = cell_width*n_cell_width+(n_cell_width-1)*cell_cell_gap_y+2*perimeter_margin    # total width of the panel

clip_thick = 6.0/1000            # open space of frame (parameter d)

seal_length = 2.0/1000           # width of seal (distance from panel edge to frame, parameter f)
seal_thick = (clip_thick-panel_thick)/2    # distance from top of panel to fram (parameter e)

frame_thick = 1.5/1000            # thickness of frame (paramater t)

c = 12.0/1000
b = 4.0/1000
a = 35.0/1000
h = 50.0/1000

cover_length = c-frame_thick-seal_length   # covered length of panel at each edge.

frame_extended = 0.1                       # the frame is created longer than panel then the extended part is cutted off

surface_extended  =  0.5                   # a surface is created to cut the frame, the surface is created bigger than panel.

#########################################
# create panel geometry
#########################################

gmsh.initialize()
gmsh.model.add("panel")


#########################################
# create frame geometry
#########################################

# create the left frame
whole_frame_surface_xy_plane = gmsh.model.occ.add_rectangle(-seal_length-frame_thick, seal_thick+frame_thick+panel_thick-h, 0, a,h)
subtract_frame_surface_1_xy_plane = gmsh.model.occ.add_rectangle(2*frame_thick+b-seal_length-frame_thick, seal_thick+frame_thick+panel_thick-h+frame_thick, 0, a-2*frame_thick-b, h-3*frame_thick-2*seal_thick-panel_thick)
subtract_frame_surface_2_xy_plane = gmsh.model.occ.add_rectangle(cover_length, -seal_thick-frame_thick, 0, a-c, 2*frame_thick+2*seal_thick+panel_thick)
subtract_frame_surface_3_xy_plane = gmsh.model.occ.add_rectangle(-seal_length, -seal_thick,0, cover_length+seal_length, 2*seal_thick+panel_thick)
subtract_frame_surface_4_xy_plane = gmsh.model.occ.add_rectangle(-seal_length, seal_thick+frame_thick+panel_thick-h+frame_thick, 0, b, h-3*frame_thick-2*seal_thick-panel_thick)

frame_surface_xz = subtract_frame_surface_4_xy_plane+1
gmsh.model.occ.cut([(2, whole_frame_surface_xy_plane)], [(2, subtract_frame_surface_1_xy_plane),(2, subtract_frame_surface_2_xy_plane),(2, subtract_frame_surface_3_xy_plane),(2, subtract_frame_surface_4_xy_plane)], tag = frame_surface_xz)

gmsh.model.occ.rotate([(2,frame_surface_xz)], 0,0,0,1,0,0,math.pi/2)

gmsh.model.occ.translate([(2,frame_surface_xz)],0,-seal_length-frame_extended,0)

left_frame = gmsh.model.occ.extrude([(2, frame_surface_xz)], 0,panel_width+2*seal_length+2*frame_extended,0)

left_frame_tag = left_frame[1][1]


# create the front frame

frame_surface_yz = gmsh.model.occ.copy([(2,frame_surface_xz)])

gmsh.model.occ.rotate(frame_surface_yz, 0,0,0,0,0,1,math.pi/2)
gmsh.model.occ.translate(frame_surface_yz,-seal_length-2*frame_extended,0,0)

front_frame = gmsh.model.occ.extrude(frame_surface_yz, panel_length+2*seal_length+2*frame_extended,0,0)

front_frame_tag = front_frame[1][1]

# create the right frame
frame_surface_right = gmsh.model.occ.copy(frame_surface_yz)
gmsh.model.occ.translate(frame_surface_right, frame_extended+panel_length+seal_length,0,0)
gmsh.model.occ.rotate(frame_surface_right, panel_length,0,0,0,0,1,math.pi/2)
gmsh.model.occ.translate(frame_surface_right, 0,-seal_length-frame_extended,0)
right_frame = gmsh.model.occ.extrude(frame_surface_right, 0,2*frame_extended+2*seal_length+panel_width,0)
right_frame_tag = right_frame[1][1]

# create the rear frame
frame_surface_rear = gmsh.model.occ.copy([(2,frame_surface_xz)])
gmsh.model.occ.translate(frame_surface_rear,0, frame_extended+panel_width+2*seal_length,0)
gmsh.model.occ.rotate(frame_surface_rear, 0,panel_width,0,0,0,1,-math.pi/2)
gmsh.model.occ.translate(frame_surface_rear,-seal_length-frame_extended, 0,0)
rear_frame = gmsh.model.occ.extrude(frame_surface_rear, 2*frame_extended+panel_length+2*seal_length,0,0)

rear_frame_tag = rear_frame[1][1]


"""
cut the frame and remove extended parts
"""
# create cutting surface at the left-front corner
cut_surface_left_front_point1 = gmsh.model.occ.addPoint(-surface_extended, -surface_extended, -surface_extended)
cut_surface_left_front_point2 = gmsh.model.occ.addPoint(surface_extended, surface_extended, -surface_extended)
cut_surface_left_front_point3 = gmsh.model.occ.addPoint(surface_extended, surface_extended, surface_extended)
cut_surface_left_front_point4 = gmsh.model.occ.addPoint(-surface_extended, -surface_extended, surface_extended)

cut_surface_left_front_line1 = gmsh.model.occ.addLine(cut_surface_left_front_point1,cut_surface_left_front_point2)
cut_surface_left_front_line2 = gmsh.model.occ.addLine(cut_surface_left_front_point2,cut_surface_left_front_point3)
cut_surface_left_front_line3 = gmsh.model.occ.addLine(cut_surface_left_front_point3,cut_surface_left_front_point4)
cut_surface_left_front_line4 = gmsh.model.occ.addLine(cut_surface_left_front_point4,cut_surface_left_front_point1)

cut_surface_left_front_curve_loop = gmsh.model.occ.addCurveLoop([cut_surface_left_front_line1,cut_surface_left_front_line2,cut_surface_left_front_line3,cut_surface_left_front_line4])

cut_surface_left_front = gmsh.model.occ.addPlaneSurface([cut_surface_left_front_curve_loop])

# create cutting surface at the right-rear corner
cut_surface_right_rear = gmsh.model.occ.copy([(2,cut_surface_left_front)])
gmsh.model.occ.translate(cut_surface_right_rear,panel_length, panel_width,0)
cut_surface_right_rear_tag = cut_surface_right_rear[0][1]

# create cutting surface at the left-rear corner
cut_surface_left_rear_point1 = gmsh.model.occ.addPoint(-surface_extended, panel_width+surface_extended, -surface_extended)
cut_surface_left_rear_point2 = gmsh.model.occ.addPoint(surface_extended, panel_width-surface_extended, -surface_extended)
cut_surface_left_rear_point3 = gmsh.model.occ.addPoint(surface_extended, panel_width-surface_extended, surface_extended)
cut_surface_left_rear_point4 = gmsh.model.occ.addPoint(-surface_extended, panel_width+surface_extended, surface_extended)

cut_surface_left_rear_line1 = gmsh.model.occ.addLine(cut_surface_left_rear_point1,cut_surface_left_rear_point2)
cut_surface_left_rear_line2 = gmsh.model.occ.addLine(cut_surface_left_rear_point2,cut_surface_left_rear_point3)
cut_surface_left_rear_line3 = gmsh.model.occ.addLine(cut_surface_left_rear_point3,cut_surface_left_rear_point4)
cut_surface_left_rear_line4 = gmsh.model.occ.addLine(cut_surface_left_rear_point4,cut_surface_left_rear_point1)

cut_surface_left_rear_curve_loop = gmsh.model.occ.addCurveLoop([cut_surface_left_rear_line1,cut_surface_left_rear_line2,cut_surface_left_rear_line3,cut_surface_left_rear_line4])

cut_surface_left_rear = gmsh.model.occ.addPlaneSurface([cut_surface_left_rear_curve_loop])

# create cutting surface at the right-front corner
cut_surface_right_front = gmsh.model.occ.copy([(2,cut_surface_left_rear)])
gmsh.model.occ.translate(cut_surface_right_front,panel_length, -panel_width,0)
cut_surface_right_front_tag = cut_surface_right_front[0][1]


# cut and remove the extended frame
cutted_left_frame = gmsh.model.occ.fragment([(3,left_frame_tag)],[(2,cut_surface_left_front), (2,cut_surface_left_rear)], removeTool=False)
gmsh.model.occ.remove([cutted_left_frame[0][0], cutted_left_frame[0][2]], recursive=True)
final_left_frame_tag = cutted_left_frame[0][1][1]
gmsh.model.occ.remove([cutted_left_frame[0][-2],cutted_left_frame[0][-3],cutted_left_frame[0][-5],cutted_left_frame[0][-6]], recursive=True)

cutted_front_frame = gmsh.model.occ.fragment([(3,front_frame_tag)],[(2,cut_surface_left_front), (2,cut_surface_right_front_tag)], removeTool=False)
gmsh.model.occ.remove([cutted_front_frame[0][0], cutted_front_frame[0][2]], recursive=True)
final_front_frame_tag = cutted_front_frame[0][1][1]
gmsh.model.occ.remove([cutted_front_frame[0][-2],cutted_front_frame[0][-3],cutted_front_frame[0][-5],cutted_front_frame[0][-6]], recursive=True)

cutted_right_frame = gmsh.model.occ.fragment([(3,right_frame_tag)],[(2,cut_surface_right_front_tag), (2,cut_surface_right_rear_tag)], removeTool=False)
gmsh.model.occ.remove([cutted_right_frame[0][0], cutted_right_frame[0][2]], recursive=True)
final_right_frame_tag = cutted_right_frame[0][1][1]
gmsh.model.occ.remove([cutted_right_frame[0][-2],cutted_right_frame[0][-3],cutted_right_frame[0][-5],cutted_right_frame[0][-6]], recursive=True)

cutted_rear_frame = gmsh.model.occ.fragment([(3,rear_frame_tag)],[(2,cut_surface_right_rear_tag), (2,cut_surface_left_rear)], removeTool=False)
gmsh.model.occ.remove([cutted_rear_frame[0][0], cutted_rear_frame[0][2]], recursive=True)
final_rear_frame_tag = cutted_rear_frame[0][1][1]
gmsh.model.occ.remove([cutted_rear_frame[0][-2],cutted_rear_frame[0][-3],cutted_rear_frame[0][-5],cutted_rear_frame[0][-6]], recursive=True)

# remove surfaces used to cut frames
gmsh.model.occ.remove([(2,cut_surface_right_rear_tag), (2,cut_surface_left_rear),(2,cut_surface_right_front_tag), (2,cut_surface_left_front) ], recursive=True)
# remove interfaces between frames, all tags of frames are not changed
gmsh.model.occ.fragment([(3, final_front_frame_tag),(3, final_rear_frame_tag)],[(3, final_left_frame_tag), (3, final_right_frame_tag)])


###########################
# create the panel
###########################
# create backsheet
back_sheet = gmsh.model.occ.addBox(0, 0, 0, panel_length, panel_width, back_sheet_thick)

# create back encapsulant layer
back_encap = gmsh.model.occ.addBox(0, 0, back_sheet_thick, panel_length, panel_width, back_encap_thick)

# create cell layer
cell_layer = gmsh.model.occ.addBox(0, 0, back_sheet_thick+back_encap_thick, panel_length, panel_width, cell_thick)

# create front encapsulant layer
front_encap = gmsh.model.occ.addBox(0, 0, back_sheet_thick+back_encap_thick+cell_thick, panel_length, panel_width, front_encap_thick)

# create front glass layer
front_glass = gmsh.model.occ.addBox(0, 0, back_sheet_thick+back_encap_thick+cell_thick+front_encap_thick, panel_length, panel_width, front_glass_thick)

# create cell
z_start_cell = back_sheet_thick+back_encap_thick
cell_list = []
for i in range(n_cell_length):
    for j in range(n_cell_width):
        cell_tag = front_glass+1+i*n_cell_width+j
        x_cell = perimeter_margin+(cell_length+cell_cell_gap_x)*i
        y_cell = perimeter_margin+(cell_width+cell_cell_gap_y)*j
        gmsh.model.occ.addBox(x_cell, y_cell, z_start_cell, cell_length, cell_width, cell_thick, tag=cell_tag)
        cell_list.append((3,cell_tag))

# remove repeated surfaces between cell and cell_layer, index of cells are not changed, index of residual cell_layer_eva is changed
cell_eva_frag = gmsh.model.occ.fragment([(3,cell_layer)], cell_list, removeTool=True)
cell_layer_encap_tag = cell_eva_frag[1][0][0][1]

gmsh.model.occ.fragment([(3,front_glass)], [(3,front_encap)], removeTool=True) # remove repeated interfaces, index of glass and front_enc are not changed
gmsh.model.occ.fragment([(3,front_encap)], cell_eva_frag[0], removeTool=True) # remove repeated interfaces, all index of involved volumes are not changed
gmsh.model.occ.fragment(cell_eva_frag[0], [(3,back_encap)], removeTool=True) # remove repeated interfaces, all index of involved volumes are not changed
gmsh.model.occ.fragment([(3,back_encap)], [(3,back_sheet)], removeTool=True) # index of each layer are not changed.

#########################################
# create seal layer geometry
#########################################

# create the seal
seal_whole = gmsh.model.occ.addBox(-seal_length, -seal_length, -seal_thick, panel_length+2*seal_length, panel_width+2*seal_length, panel_thick+2*seal_thick)
remove_seal_1 = gmsh.model.occ.addBox(cover_length, cover_length, -seal_thick, panel_length-2*(cover_length), panel_width-2*(cover_length), panel_thick+2*seal_thick)
remove_seal_2 = gmsh.model.occ.addBox(0,0,0, panel_length, panel_width, panel_thick)
seal = remove_seal_2+1
gmsh.model.occ.cut([(3, seal_whole)], [(3, remove_seal_1), (3, remove_seal_2)], tag = seal)

# romove repeated interfaces between panel and seal, 
gmsh.model.occ.fragment([(3,seal)],[(3, front_glass),(3, front_encap),(3, cell_layer_encap_tag),(3,back_encap),(3,back_sheet)], removeTool=True)

# remove interfaces between frame and seal, all volume index are not changd
gmsh.model.occ.fragment([(3, final_front_frame_tag),(3, final_rear_frame_tag),(3, final_left_frame_tag), (3, final_right_frame_tag)],[(3,seal)], removeTool=True)


gmsh.model.occ.synchronize()
gmsh.write("panel_geo.brep")




# #######################
# # create mesh
# #######################

# gmsh.option.setNumber('Mesh.MeshSizeMin', 0.001)
# gmsh.option.setNumber('Mesh.MeshSizeMax', 0.001)

# gmsh.model.mesh.generate(3)
# gmsh.write('panel.vtk')

# gmsh.finalize()
