import numpy as np
import gmsh
import math


"""
create surface and volume marker
"""

def volume_tags(vol_list,count_volumes,structure_vol_list, number_volume_groups): # number_volumes = number of cells + 4 (frames) +1(seal) + 5(glass, eva,eva,eva,backsheet)
    for i in range(number_volume_groups):
        _add_to_domain_markers(structure_vol_list[count_volumes], vol_list[count_volumes], "cell")
        count_volumes+=1
    return count_volumes

def surface_tags(surf_list,count_surface):
    for surf_tag in surf_list:
                surf_id = surf_tag[1]
                # com = gmsh.model.occ.getCenterOfMass(ndim - 1, surf_id)
                _add_to_domain_markers("sur"+str(surf_id), [surf_id], "facet")
                count_surface +=1
    return count_surface

def _add_to_domain_markers(marker_name, gmsh_tags, entity_type):
    # Create a dictionary to hold the gmsh tags associated with
    # entity name and type

    assert isinstance(gmsh_tags, list)
    assert entity_type in ["cell", "facet"]

    marker_dict = {
        "idx": domain_markers["_current_idx"],
        "gmsh_tags": gmsh_tags,
        "entity": entity_type,
    }

    domain_markers[marker_name] = marker_dict
    domain_markers["_current_idx"] += 1

"""
create physical groups
"""
def from_domain_markers_to_PhysicalName(domain_markers,ndim):
    # set physical attributes
    for key, data in domain_markers.items():
                if isinstance(data, dict) and "gmsh_tags" in data:
                    # print(key)
                    # Cells (i.e., entities of dim = msh.topology.dim)
                    if data["entity"] == "cell":
                        gmsh.model.addPhysicalGroup(
                            ndim, data["gmsh_tags"], data["idx"]
                        )
                        gmsh.model.setPhysicalName(ndim, data["idx"], key)

                    # Facets (i.e., entities of dim = msh.topology.dim - 1)
                    if data["entity"] == "facet":
                        gmsh.model.addPhysicalGroup(
                            ndim - 1, data["gmsh_tags"], data["idx"]
                        )
                        gmsh.model.setPhysicalName(ndim - 1, data["idx"], key)

"""
process the input from input file
"""
def process_input_file(input_file_path):
    # Initialize variables
    cell_thick = ''
    n_cell_length = ''       
    n_cell_width = ''      
    front_glass_thick = ''   
    front_encap_thick= ''    
    back_encap_thick= ''   
    file_format= ''  
    cell_length= ''
    cell_width= ''
    back_sheet_thick= ''
    perimeter_margin= ''
    cell_cell_gap_x = ''
    cell_cell_gap_y = ''
    clip_thick=''
    seal_length=''
    frame_thick=''

    c = ''
    b = ''
    a = ''
    h = ''

    mesh_size_in_cell = ''
    mesh_size_out_cell = ''

    mounting_area_shape = '' 
    mounting_area_size = '' 
    mounting_location = ''

    # Read input values from the text file
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"{input_file_path} not found. Reading from original.txt instead.")
        input_file_path = "original.txt"
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

    for line in lines:
        key, value = line.strip().split(": ")
        if key == "cell_thick":
            cell_thick = value
        elif key == "n_cell_length":
            n_cell_length = value
        elif key == "n_cell_width":
            n_cell_width = value
        elif key == "front_glass_thick":
            front_glass_thick = value
        elif key == "front_encap_thick":
            front_encap_thick = value
        elif key == "back_encap_thick":
            back_encap_thick = value
        elif key == "file_format":
            file_format = value
        elif key == "cell_width":
            cell_width = value
        elif key == "cell_length":
            cell_length = value
        elif key == "back_sheet_thick":
            back_sheet_thick = value
        elif key == "perimeter_margin":
            perimeter_margin = value
        elif key == "cell_cell_gap_x":
            cell_cell_gap_x = value
        elif key == "cell_cell_gap_y":
            cell_cell_gap_y = value
        elif key == "clip_thick":
            clip_thick = value
        elif key == "seal_length":
            seal_length = value
        elif key == "frame_thick":
            frame_thick = value
        elif key == "a":
            a = value 
        elif key == "b":
            b = value 
        elif key == "c":
            c = value 
        elif key == "h":
            h = value 
        elif key == "mesh_size_in_cell":
            mesh_size_in_cell = value
        elif key == "mesh_size_out_cell":
            mesh_size_out_cell = value
        elif key == "mounting_area_shape":
            mounting_area_shape = value
        elif key == "mounting_area_size":
            mounting_area_size = value
        elif key == "mounting_location":
            mounting_location = value
       

    # Print the variables (replace with your processing logic)
    # print("cell_thick:", cell_thick)
    # print("n_cell_length:", n_cell_length)
    # print("n_cell_width:", n_cell_width)
    # print("front_glass_thick:", front_glass_thick)
    # print("front_encap_thick:", front_encap_thick)
    # print("back_encap_thick:", back_encap_thick)
    # print("file_format:", file_format)

    print("input func finished")

    return float(cell_thick), int(n_cell_length) , int(n_cell_width), float(front_glass_thick) ,\
          float(front_encap_thick), float(back_encap_thick), float(cell_length), float(cell_width) ,\
              float(back_sheet_thick), file_format, float(perimeter_margin), float(cell_cell_gap_x), \
                float(cell_cell_gap_y), float(clip_thick), float(seal_length), float(frame_thick),\
                float(a), float(b), float(c), float(h), float(mesh_size_in_cell), float(mesh_size_out_cell), \
                mounting_area_shape, float(mounting_area_size), float(mounting_location)

"""
define parameters
"""
input_file_path = "input.txt"  # Replace with the actual path of the input file
cell_thick, n_cell_length , n_cell_width, front_glass_thick ,\
      front_encap_thick, back_encap_thick, cell_length, cell_width , \
        back_sheet_thick , file_format, perimeter_margin, cell_cell_gap_x ,\
              cell_cell_gap_y, clip_thick, seal_length, frame_thick , a, b,c, h, \
                  mesh_size_in_cell, mesh_size_out_cell, \
                mounting_area_shape, mounting_area_size, mounting_location  = process_input_file(input_file_path)


"""
code to generate PV panel geometry and mesh
"""
# cell_thick = 0.17   # thick ness of cell in mm
#n_cell_length = 12       # number of cells along x
#n_cell_width = 6         # number of cells along y
#front_glass_thick = 3.2  # thickness of gront glass layer
front_encap_thick = front_encap_thick-cell_thick/2    # thickness of front encapsulant layer, in mm
back_encap_thick = back_encap_thick-cell_thick/2     # thickness of back encapsulant layer, in mm
# cell_length = 182.0      # length of each cell in mm 
# cell_width = 182.0      # width of each cell in mm
# back_sheet_thick = 0.35     # thickness of backsheet or back glass, in mm
# perimeter_margin = 10.0  # edge margin in mm
# cell_cell_gap_x = 2.5  # gap between cell along x, in mm
# cell_cell_gap_y = 2.5  # gap between cell along y, in mm
# clip_thick = 6.0            # open space of frame (parameter d, d-2e is panel thickness), in mm
# seal_length = 2.0           # width of seal (distance from panel edge to frame, parameter f), in mm
# frame_thick = 1.5           # thickness of frame (paramater t) in mm
# a = 35.0 # in mm
# b = 4.0 # in mm
# c = 12.0 # in mm
# h = 50.0 # in mm
# # the following size works well for the case without mounting area
# mesh_size_in_cell = 12
# mesh_size_out_cell = 4.5

# # for case with mounting area: # # the following size works well for the case with mounting area
# mesh_size_in_cell = 12
# mesh_size_out_cell = 3

# mounting_area_shape = 'square' # shape of mounting area, square or circle
# mounting_area_size = 10 #in mm, it is the circle diameter (circle area) or edge length (square)

# mounting_location = 0.3  # twp mounting areas per edge, 0.3*total length and (1-0.3) * total length


panel_thick = cell_thick+front_glass_thick+front_encap_thick+back_encap_thick+back_sheet_thick
panel_length = cell_length*n_cell_length+(n_cell_length-1)*cell_cell_gap_x+2*perimeter_margin    # total length of the panel
panel_width = cell_width*n_cell_width+(n_cell_width-1)*cell_cell_gap_y+2*perimeter_margin    # total width of the panel

seal_thick = (clip_thick-panel_thick)/2    # distance from top of panel to fram (parameter e)

cover_length = c-frame_thick-seal_length   # covered length of panel at each edge.

frame_extended = 0.1*cell_length                       # the frame is created longer than panel then the extended part is cutted off

surface_extended  =  500                   # a surface is created to cut the frame, the surface is created bigger than panel. in mm

ndim = 3

gmsh.initialize()
gmsh.model.add("panel")

# Turn off printed output to the terminal
# gmsh.option.setNumber("General.Terminal", 0)

"""
create frame geometry
"""

#########################
# create the left frame
#########################

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

#########################
# create the front frame
#########################

frame_surface_yz = gmsh.model.occ.copy([(2,frame_surface_xz)])

gmsh.model.occ.rotate(frame_surface_yz, 0,0,0,0,0,1,math.pi/2)
gmsh.model.occ.translate(frame_surface_yz,-2*seal_length-2*frame_extended,0,0)

front_frame = gmsh.model.occ.extrude(frame_surface_yz, panel_length+2*seal_length+2*frame_extended,0,0)

front_frame_tag = front_frame[1][1]

#########################
# create the right frame
#########################

frame_surface_right = gmsh.model.occ.copy(frame_surface_yz)
gmsh.model.occ.translate(frame_surface_right, 2*frame_extended+panel_length+2*seal_length,0,0)
gmsh.model.occ.rotate(frame_surface_right, panel_length,0,0,0,0,1,math.pi/2)
gmsh.model.occ.translate(frame_surface_right, 0,-2*seal_length-2*frame_extended,0)
right_frame = gmsh.model.occ.extrude(frame_surface_right, 0,2*frame_extended+2*seal_length+panel_width,0)
right_frame_tag = right_frame[1][1]



#########################
# create the rear frame
##########################

frame_surface_rear = gmsh.model.occ.copy([(2,frame_surface_xz)])
gmsh.model.occ.translate(frame_surface_rear,0, 2*frame_extended+panel_width+2*seal_length,0)
gmsh.model.occ.rotate(frame_surface_rear, 0,panel_width,0,0,0,1,-math.pi/2)
gmsh.model.occ.translate(frame_surface_rear,-2*seal_length-2*frame_extended, 0,0)
rear_frame = gmsh.model.occ.extrude(frame_surface_rear, 2*frame_extended+panel_length+2*seal_length,0,0)
rear_frame_tag = rear_frame[1][1]

"""
cut the frame and remove extended parts
"""
###################################################
# create cutting surface at the left-front corner
###################################################

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

###################################################
# create cutting surface at the right-rear corner
###################################################

cut_surface_right_rear = gmsh.model.occ.copy([(2,cut_surface_left_front)])

gmsh.model.occ.translate(cut_surface_right_rear,panel_length, panel_width,0)

cut_surface_right_rear_tag = cut_surface_right_rear[0][1]

###################################################
# create cutting surface at the left-rear corner
###################################################

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

###################################################
# create cutting surface at the right-front corner
###################################################

cut_surface_right_front = gmsh.model.occ.copy([(2,cut_surface_left_rear)])
gmsh.model.occ.translate(cut_surface_right_front,panel_length, -panel_width,0)
cut_surface_right_front_tag = cut_surface_right_front[0][1]


###################################################
# cut and remove the extended part of left frame
###################################################
cutted_left_frame = gmsh.model.occ.fragment([(3,left_frame_tag)],[(2,cut_surface_left_front), (2,cut_surface_left_rear)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_left_frame[0][0], cutted_left_frame[0][2]], recursive=True)
# final tag of frame at left
final_left_frame_tag = cutted_left_frame[0][1][1] # scalar
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_left_frame[0])[0]):
    remove_surface_list.append(cutted_left_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)



###################################################
# cut and remove the extended part of front frame
###################################################

cutted_front_frame = gmsh.model.occ.fragment([(3,front_frame_tag)],[(2,cut_surface_left_front), (2,cut_surface_right_front_tag)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_front_frame[0][0], cutted_front_frame[0][2]], recursive=True)
# final tag of frame at front
final_front_frame_tag = cutted_front_frame[0][1][1] # scalar
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_front_frame[0])[0]):
    remove_surface_list.append(cutted_front_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)

###################################################
# cut and remove the extended part of right frame
###################################################

cutted_right_frame = gmsh.model.occ.fragment([(3,right_frame_tag)],[(2,cut_surface_right_front_tag), (2,cut_surface_right_rear_tag)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_right_frame[0][0], cutted_right_frame[0][2]], recursive=True)
# final tag of frame at right
final_right_frame_tag = cutted_right_frame[0][1][1] # scalar
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_right_frame[0])[0]):
    remove_surface_list.append(cutted_right_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)

###################################################
# cut and remove the extended part of rear frame
###################################################

cutted_rear_frame = gmsh.model.occ.fragment([(3,rear_frame_tag)],[(2,cut_surface_right_rear_tag), (2,cut_surface_left_rear)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_rear_frame[0][0], cutted_rear_frame[0][2]], recursive=True)
# final tag of frame at rear
final_rear_frame_tag = cutted_rear_frame[0][1][1] # scalar
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_rear_frame[0])[0]):
    remove_surface_list.append(cutted_rear_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)

# remove surfaces used to cut frames
gmsh.model.occ.remove([(2,cut_surface_right_rear_tag), (2,cut_surface_left_rear),(2,cut_surface_right_front_tag), (2,cut_surface_left_front) ], recursive=True)
# remove interfaces between frames, all tags of frames are not changed
gmsh.model.occ.fragment([(3, final_front_frame_tag),(3, final_rear_frame_tag)],[(3, final_left_frame_tag), (3, final_right_frame_tag)])


"""
create panel
"""
##################################
# create the panel (unpartitioned)
##################################

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



#################################################################################################
# since the top surface and bottom surface of the panel are partially covered by the seal, 
# we partition the whole thickness of the panel to have a covered volume for each layer, 
# so we can have a sweep mesh

# partition of front glass into covered and uncovered part:
#################################################################################################

# create volume to partition front glass
z_start_cell_front_glass = back_sheet_thick+back_encap_thick+cell_thick+front_encap_thick

# partition the glass into two parts, uncovered part and covered part
uncovered_glass = gmsh.model.occ.addBox(cover_length, cover_length, z_start_cell_front_glass, panel_length-2*cover_length, \
                                        panel_width-2*cover_length, front_glass_thick)
uncovered_front_glass_frag = gmsh.model.occ.fragment([(3,front_glass)],[(3,uncovered_glass)], removeTool=True)

# uncovered_front_glass_frag[0][0][1] is uncovered part, uncovered_front_glass_frag[0][1][1] is the covered part

#################################################################################################
# since the cell layer has different geometry compared to other layers (include cells), we 
# partite each layer to make them has the same geometry as cell layer

# partition of front glass by cells.
#################################################################################################

cell_front_glass_list = [] # vector array
for i in range(n_cell_length):
    for j in range(n_cell_width):
        cell_tag = uncovered_front_glass_frag[0][1][1]+1+i*n_cell_width+j
        x_cell = perimeter_margin+(cell_length+cell_cell_gap_x)*i
        y_cell = perimeter_margin+(cell_width+cell_cell_gap_y)*j
        gmsh.model.occ.addBox(x_cell, y_cell, z_start_cell_front_glass, cell_length, cell_width, front_glass_thick, tag=cell_tag)
        cell_front_glass_list.append((3,cell_tag))

# partition of uncovered front_glass
cell_front_glass_frag = gmsh.model.occ.fragment([(3,uncovered_front_glass_frag[0][0][1])], cell_front_glass_list, removeTool=True)
front_glass_tag_list = cell_front_glass_frag[0] #list of vector, uncovered part
front_glass_tag_list.append(uncovered_front_glass_frag[0][1]) # covered part

###################################################
# partition of front eva
###################################################

# create volume to partition front eva
z_start_cell_front_eva = back_sheet_thick+back_encap_thick+cell_thick

# partition the front_eva into two parts, uncovered part and covered part
uncovered_front_eva = gmsh.model.occ.addBox(cover_length, cover_length, z_start_cell_front_eva, panel_length-2*cover_length, \
                                        panel_width-2*cover_length, front_encap_thick)

uncovered_front_eva_frag = gmsh.model.occ.fragment([(3,front_encap)],[(3,uncovered_front_eva)], removeTool=True)

# uncovered_front_eva_frag[0][0][1] is uncovered part, uncovered_front_eva_frag[0][1][1] is the covered part

cell_front_eva_list = []
for i in range(n_cell_length):
    for j in range(n_cell_width):
        cell_tag = uncovered_front_eva_frag[0][1][1]+1+i*n_cell_width+j
        x_cell = perimeter_margin+(cell_length+cell_cell_gap_x)*i
        y_cell = perimeter_margin+(cell_width+cell_cell_gap_y)*j
        gmsh.model.occ.addBox(x_cell, y_cell, z_start_cell_front_eva, cell_length, cell_width, front_encap_thick, tag=cell_tag)
        cell_front_eva_list.append((3,cell_tag))
# partition of front eva layer
cell_front_eva_frag = gmsh.model.occ.fragment([(3,uncovered_front_eva_frag[0][0][1])], cell_front_eva_list, removeTool=True)
front_encap_tag_list = cell_front_eva_frag[0] # list of vector
front_encap_tag_list.append(uncovered_front_eva_frag[0][1])


###################################################
# partition of the back eva
###################################################

# create volume to partition back eva
z_start_cell_back_eva = back_sheet_thick

# partition the back_eva into two parts, uncovered part and covered part
uncovered_back_eva = gmsh.model.occ.addBox(cover_length, cover_length, z_start_cell_back_eva, panel_length-2*cover_length, \
                                        panel_width-2*cover_length, back_encap_thick)

uncovered_back_eva_frag = gmsh.model.occ.fragment([(3,back_encap)],[(3,uncovered_back_eva)], removeTool=True)

# uncovered_beack_eva_frag[0][0][1] is uncovered part, uncovered_back_eva_frag[0][1][1] is the covered part

cell_back_eva_list = []
for i in range(n_cell_length):
    for j in range(n_cell_width):
        cell_tag = uncovered_back_eva_frag[0][1][1]+1+i*n_cell_width+j
        x_cell = perimeter_margin+(cell_length+cell_cell_gap_x)*i
        y_cell = perimeter_margin+(cell_width+cell_cell_gap_y)*j
        gmsh.model.occ.addBox(x_cell, y_cell, z_start_cell_back_eva, cell_length, cell_width, back_encap_thick, tag=cell_tag)
        cell_back_eva_list.append((3,cell_tag))
# partition of back eva layer
cell_back_eva_frag = gmsh.model.occ.fragment([(3,uncovered_back_eva_frag[0][0][1])], cell_back_eva_list, removeTool=True)
back_encap_tag_list = cell_back_eva_frag[0] # list of vector
back_encap_tag_list.append(uncovered_back_eva_frag[0][1])

###################################################
# partition of cell layer
###################################################

# create volume to partition cell layer
z_start_cell_cell_layer = back_sheet_thick + back_encap_thick

# partition the back_eva into two parts, uncovered part and covered part
uncovered_cell_layer = gmsh.model.occ.addBox(cover_length, cover_length, z_start_cell_cell_layer, panel_length-2*cover_length, \
                                        panel_width-2*cover_length, cell_thick)

uncovered_cell_layer_frag = gmsh.model.occ.fragment([(3,cell_layer)],[(3,uncovered_cell_layer)], removeTool=True)

# uncovered_cell_layer_frag[0][0][1] is uncovered part, uncovered_cell_layer_frag[0][1][1] is the covered part

# create cell
cell_list = []
for i in range(n_cell_length):
    for j in range(n_cell_width):
        cell_tag = uncovered_cell_layer_frag[0][1][1]+1+i*n_cell_width+j
        x_cell = perimeter_margin+(cell_length+cell_cell_gap_x)*i
        y_cell = perimeter_margin+(cell_width+cell_cell_gap_y)*j
        gmsh.model.occ.addBox(x_cell, y_cell, z_start_cell_cell_layer, cell_length, cell_width, cell_thick, tag=cell_tag)
        cell_list.append((3,cell_tag))

# remove repeated surfaces between cell and cell_layer, index of cells are not changed, index of residual cell_layer_eva is changed
cell_eva_frag = gmsh.model.occ.fragment([(3,uncovered_cell_layer_frag[0][0][1])], cell_list, removeTool=True)    # cell_layer is partited to be 1+n_cell_length*n_cell_width, cell are partited into 2*n_cell_length*n_cell_width

whole_cell_layer = cell_eva_frag[1][0] # list of vector
whole_cell_layer.append(uncovered_cell_layer_frag[0][1]) # list of vector

cell_layer_encap_tag = [x[1] for x in whole_cell_layer if x not in cell_list]  # tag of eva domain in cell layer, list of single scalar


# ##################################################
# partition of the back sheet
# ##################################################

# create volume to partition back sheet
z_start_cell_back_sheet = 0

# partition the back_sheet into two parts, uncovered part and covered part
uncovered_back_sheet = gmsh.model.occ.addBox(cover_length, cover_length, z_start_cell_back_sheet, panel_length-2*cover_length, \
                                        panel_width-2*cover_length, back_sheet_thick)

uncovered_back_sheet_frag = gmsh.model.occ.fragment([(3,back_sheet)],[(3,uncovered_back_sheet)], removeTool=True)

# uncovered_back_sheet_frag[0][0][1] is uncovered part, uncovered_back_sheet_frag[0][1][1] is the covered part

cell_back_sheet_list = []
for i in range(n_cell_length):
    for j in range(n_cell_width):
        cell_tag = uncovered_back_sheet_frag[0][1][1]+1+i*n_cell_width+j
        x_cell = perimeter_margin+(cell_length+cell_cell_gap_x)*i
        y_cell = perimeter_margin+(cell_width+cell_cell_gap_y)*j
        gmsh.model.occ.addBox(x_cell, y_cell, z_start_cell_back_sheet, cell_length, cell_width, back_sheet_thick, tag=cell_tag)
        cell_back_sheet_list.append((3,cell_tag))
#partition of back sheet
cell_back_sheet_frag = gmsh.model.occ.fragment([(3,uncovered_back_sheet_frag[0][0][1])], cell_back_sheet_list, removeTool=True)
back_sheet_tag_list = cell_back_sheet_frag[1][0]   # list of vector
back_sheet_tag_list.append(uncovered_back_sheet_frag[0][1])



gmsh.model.occ.fragment(front_glass_tag_list, front_encap_tag_list, removeTool=True) # remove repeated interfaces, index of glass and front_enc are not changed
gmsh.model.occ.fragment(front_encap_tag_list, whole_cell_layer, removeTool=True) # remove repeated interfaces, all index of involved volumes are not changed
gmsh.model.occ.fragment(whole_cell_layer, back_encap_tag_list, removeTool=True) # remove repeated interfaces, all index of involved volumes are not changed
gmsh.model.occ.fragment(back_encap_tag_list, back_sheet_tag_list, removeTool=True) # index of each layer are not changed.


"""
create seal layer geometry
"""

###################
# create the seal
####################
seal_whole = gmsh.model.occ.addBox(-seal_length, -seal_length, -seal_thick, panel_length+2*seal_length, panel_width+2*seal_length, panel_thick+2*seal_thick)
remove_seal_1 = gmsh.model.occ.addBox(cover_length, cover_length, -seal_thick, panel_length-2*(cover_length), panel_width-2*(cover_length), panel_thick+2*seal_thick)
remove_seal_2 = gmsh.model.occ.addBox(0,0,0, panel_length, panel_width, panel_thick)
seal = remove_seal_2+1
gmsh.model.occ.cut([(3, seal_whole)], [(3, remove_seal_1), (3, remove_seal_2)], tag = seal)

#######################################
# fragment to remove repeated surfaces
#######################################

# romove repeated interfaces between panel and seal, 
gmsh.model.occ.fragment([(3,seal)],front_glass_tag_list+front_encap_tag_list+whole_cell_layer+back_encap_tag_list+back_sheet_tag_list, removeTool=True)

# remove interfaces between frame and seal, all volume index are not changd
gmsh.model.occ.fragment([(3, final_front_frame_tag),(3, final_rear_frame_tag),(3, final_left_frame_tag), (3, final_right_frame_tag)],[(3,seal)], removeTool=True)

"""
create mounting area
"""


mounting_location_x_1 = mounting_location*(panel_length+2*seal_length+2*frame_thick)-seal_length-frame_thick
mounting_location_x_2 = (1-mounting_location)*(panel_length+2*seal_length+2*frame_thick)-seal_length-frame_thick
mounting_location_y_1 = a/2-seal_length-frame_thick
mounting_location_y_2 = -a/2+seal_length+frame_thick+panel_width
mounting_location_z = panel_thick+seal_thick+frame_thick-h


if mounting_area_shape == 'circle':
    mounting_area_1 = gmsh.model.occ.add_cylinder(mounting_location_x_1,mounting_location_y_1, mounting_location_z,0,0,frame_thick, mounting_area_size/2)
    mounting_area_2 = gmsh.model.occ.add_cylinder(mounting_location_x_2,mounting_location_y_1, mounting_location_z,0,0,frame_thick, mounting_area_size/2)
    mounting_area_3 = gmsh.model.occ.add_cylinder(mounting_location_x_1,mounting_location_y_2, mounting_location_z,0,0,frame_thick, mounting_area_size/2)
    mounting_area_4 = gmsh.model.occ.add_cylinder(mounting_location_x_2,mounting_location_y_2, mounting_location_z,0,0,frame_thick, mounting_area_size/2)

if mounting_area_shape == 'square':
    mounting_area_1 = gmsh.model.occ.add_box(mounting_location_x_1-mounting_area_size/2,mounting_location_y_1-mounting_area_size/2, mounting_location_z, mounting_area_size,mounting_area_size, frame_thick)
    mounting_area_2 = gmsh.model.occ.add_box(mounting_location_x_2-mounting_area_size/2,mounting_location_y_1-mounting_area_size/2, mounting_location_z, mounting_area_size,mounting_area_size, frame_thick)
    mounting_area_3 = gmsh.model.occ.add_box(mounting_location_x_1-mounting_area_size/2,mounting_location_y_2-mounting_area_size/2, mounting_location_z, mounting_area_size,mounting_area_size, frame_thick)
    mounting_area_4 = gmsh.model.occ.add_box(mounting_location_x_2-mounting_area_size/2,mounting_location_y_2-mounting_area_size/2, mounting_location_z, mounting_area_size,mounting_area_size, frame_thick)

mounting_frame_frag_front = gmsh.model.occ.fragment([(3, final_front_frame_tag)],[(3,mounting_area_1), (3, mounting_area_2)], removeTool=True)
mounting_frame_frag_rear = gmsh.model.occ.fragment([(3, final_rear_frame_tag)],[(3,mounting_area_3), (3, mounting_area_4)], removeTool=True)

front_frame_extract_mounting = mounting_frame_frag_front[0][2][1] # scalar
mounting_1_tag = mounting_frame_frag_front[0][0][1]
mounting_2_tag = mounting_frame_frag_front[0][1][1]

rear_frame_extract_mounting = mounting_frame_frag_rear[0][2][1]
mounting_3_tag = mounting_frame_frag_rear[0][0][1]
mounting_4_tag = mounting_frame_frag_rear[0][1][1]

#######################################
# get tags of each layer
#######################################

front_glass_tags = [] # list of scalar
for i in range (len(front_glass_tag_list)):
    front_glass_tags.append(front_glass_tag_list[i][1])

front_encap_tags = []
for i in range (len(front_encap_tag_list)):
    front_encap_tags.append(front_encap_tag_list[i][1])

back_encap_tags = []
for i in range (len(back_encap_tag_list)):
    back_encap_tags.append(back_encap_tag_list[i][1])

back_sheet_tags = []
for i in range (len(back_sheet_tag_list)):
    back_sheet_tags.append(back_sheet_tag_list[i][1])

all_volume_list = [[final_left_frame_tag,front_frame_extract_mounting,final_right_frame_tag,rear_frame_extract_mounting],[mounting_1_tag,mounting_2_tag,mounting_3_tag,mounting_4_tag], back_sheet_tags, back_encap_tags, front_encap_tags, front_glass_tags]


cell_tags = []

for i in range(int(n_cell_length*n_cell_width)):
    cell_tags.append(cell_list[i][1])

all_volume_list.append(cell_tags)
all_volume_list.append(cell_layer_encap_tag)
all_volume_list.append([seal])


number_volume_groups = len(all_volume_list)

# all_volume_list
# [0]: volume tages of all frames, [0][0] left frame, [0][1] front frame, [0][2] right frame, [0][1] rear frame
# [1]: volume tags of mounting areas, if the mounting area is not existing, you can set the material of mounting area be very compliance
# [2]: volume tages of back sheet
# [3]: volume tages of back encap
# [4]: volume tages of front encap
# [5]: volume tages of front glass
# [6]: volume tages of all cells
# [7]: volume tages of encapsulant in cell layer, [6][0] is the uncovered part, [6][1] is the covered part
# [8]: volume tages of seal layer


gmsh.model.occ.synchronize()
gmsh.write("panel_geo.brep")


"""
mark all surfaces and volumes and create physical groups for each surface and volume
"""

## domain_markers = {surface1(domain_name): {marker id: 1, gmsh tag:[], type:facet}
#                    surface2(domain_name): {marker id: 2, gmsh tag:[], type:facet
#                                         ......(if n surfaces)
#                    surface n(domain_name): {marker id: n, gmsh tag:[], type:facet


#                    frm: {marker id: n+1, gmsh tag:[], type:cell}
#                    mounting:{marker id: n+2, gmsh tag:[], type:cell}
#                                    ......
#                    seal{maker id: n+9, gmsh rag: [seal], type: cell}

count_volumes_groups=0
count_surface = 0

domain_markers = {}                    # Must start indexing at 1, if starting at 0, things marked "0"
                                       # are indistinguishable from things which receive no marking (and have default value of 0)
domain_markers["_current_idx"] = 1

# # capture surfaces
surf_tag_list = gmsh.model.occ.getEntities(ndim - 1)  #[(dim, tag),()...]
count_surface =  surface_tags(surf_tag_list,count_surface) # number of surfaces

structure_vol_list =["frm", "mounting"]  # frm0 is left frame, frm1 is front frame, frm2 is right frame, frm3 is rear frame. 
structure_vol_list +=["back_sheet","back_encap","front_encap","front_glass", "cell", "cell_layer_encap", "seal"]


count_volumes_groups =  volume_tags(all_volume_list,count_volumes_groups,structure_vol_list, number_volume_groups)
# # domain_markers: current_idx:157, sur 100:{idx:100, tags: [100], type: facet}....front_glass:{idx: 1, tag: [20,21,3,4,3], type: cell}


# add physical group for surface and volumes. physical group 1: (name: suf 1, physical group number 1)
from_domain_markers_to_PhysicalName(domain_markers, int(ndim))




"""
create mesh size field
"""

# define box field for the whole domain
box_field_list = []
volume_field_whole_domain = gmsh.model.mesh.field.add("Box")
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "Thickness", frame_thick)  # the mesh size is interpolated between VIn and VOut in a layer around the box of the prescribed thickness.
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "VIn", mesh_size_out_cell)
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "VOut", mesh_size_out_cell)
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "XMax", panel_length+seal_length+frame_thick)
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "XMin", -seal_length-frame_thick)
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "YMax", panel_width+seal_length+frame_thick)
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "YMin", -seal_length-frame_thick)
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "ZMax", panel_thick+seal_thick+frame_thick)
gmsh.model.mesh.field.setNumber(volume_field_whole_domain, "ZMin", panel_thick+seal_thick+frame_thick-h)
box_field_list.append(volume_field_whole_domain)

# define box field for cells, box will go across whole thickness of panel
for i in range(n_cell_length):
     for j in range(n_cell_width):
        cell_volume_field = gmsh.model.mesh.field.add("Box")
        gmsh.model.mesh.field.setNumber(cell_volume_field, "Thickness", cell_cell_gap_x/2)  # the mesh size is interpolated between VIn and VOut in a layer around the box of the prescribed thickness.
        gmsh.model.mesh.field.setNumber(cell_volume_field, "VOut", mesh_size_out_cell)
        gmsh.model.mesh.field.setNumber(cell_volume_field, "VIn", mesh_size_in_cell)
        gmsh.model.mesh.field.setNumber(cell_volume_field, "XMin", perimeter_margin+(cell_length+cell_cell_gap_x)*i)
        gmsh.model.mesh.field.setNumber(cell_volume_field, "XMax", perimeter_margin+(cell_length+cell_cell_gap_x)*i+cell_length)
        gmsh.model.mesh.field.setNumber(cell_volume_field, "YMin", perimeter_margin+(cell_width+cell_cell_gap_y)*j)
        gmsh.model.mesh.field.setNumber(cell_volume_field, "YMax", perimeter_margin+(cell_width+cell_cell_gap_y)*j+cell_width)
        gmsh.model.mesh.field.setNumber(cell_volume_field, "ZMax", panel_thick)
        gmsh.model.mesh.field.setNumber(cell_volume_field, "ZMin", 0)
        box_field_list.append(cell_volume_field)

maximum = gmsh.model.mesh.field.add("Max")
gmsh.model.mesh.field.setNumbers(maximum, "FieldsList", box_field_list)  # take the minimum value of a list of fields.
gmsh.model.mesh.field.setAsBackgroundMesh(maximum)               # set the minimum field as the background mesh size field

# gmsh.model.mesh.setTransfiniteAutomatic()

gmsh.option.setNumber("Mesh.ToleranceInitialDelaunay", 1e-12)

gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 10)     #10, split a circle to how many elements


gmsh.option.setNumber("Mesh.Algorithm", 5) #2
gmsh.option.setNumber("Mesh.Algorithm3D", 1)
gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 0) #2
gmsh.model.mesh.setOrder(1)

gmsh.model.mesh.optimize('Netgen')

gmsh.model.mesh.generate(3)



"""
save mesh files
"""
# gmsh.write("panel_geo.msh")      # for ansys
# gmsh.write("panel_geo.vtk")      # for fenics?
# # gmsh.write("panel_geo.stl")
# gmsh.write("panel_geo.inp")      # for abaqus
# # gmsh.write("panel_geo.dat")      # for ansys
# # gmsh.write("panel_geo.wrl")
# gmsh.write("panel_geo.bdf")      # bdf file for comsol

if file_format == "vtk":
    gmsh.write("PV_mesh.vtk")
elif file_format == "msh":
    gmsh.write("PV_mesh.msh")
elif file_format == "inp":
    gmsh.write("PV_mesh.inp")
elif file_format == "bdf":
    gmsh.write("PV_mesh.bdf")
else: 
    "file Format not recognised"

gmsh.finalize()

print("Mesh generated")
