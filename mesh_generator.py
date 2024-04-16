import numpy as np
import gmsh
import math


"""
code to generate PV panel geometry and mesh
"""
def _add_to_domain_markers(marker_name, gmsh_tags, entity_type):
        # Create a dictionary to hold the gmsh tags associated with
        # x_min, x_max, y_min, y_max, z_min, z_max panel surfaces and domain walls

        # if not hasattr(self, "domain_markers"):
        #     self.domain_markers = {}
        #     # Must start indexing at 1, if starting at 0, things marked "0"
        #     # are indistinguishable from things which receive no marking (and have default value of 0)
        #     self.domain_markers["_current_idx"] = 1

        assert isinstance(gmsh_tags, list)
        assert entity_type in ["cell", "facet"]

        marker_dict = {
            "idx": domain_markers["_current_idx"],
            "gmsh_tags": gmsh_tags,
            "entity": entity_type,
        }

        domain_markers[marker_name] = marker_dict
        domain_markers["_current_idx"] += 1

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
                        print("added volume ", key)

                    # Facets (i.e., entities of dim = msh.topology.dim - 1)
                    if data["entity"] == "facet":
                        gmsh.model.addPhysicalGroup(
                            ndim - 1, data["gmsh_tags"], data["idx"]
                        )
                        gmsh.model.setPhysicalName(ndim - 1, data["idx"], key)

def volume_tags(vol_list,count_volumes,structure_vol_list):
    for vol_tag in vol_list:
        vol_id = vol_tag[1]
        # structure_vol_list.append("vol"+str(count_volumes))
        # _add_to_domain_markers("vol"+str(count_volumes), [vol_id], "cell")
        _add_to_domain_markers(structure_vol_list[count_volumes], [vol_id], "cell")
        # print(count_volumes)
        count_volumes+=1
    return count_volumes, structure_vol_list

def surface_tags(surf_list,count_surface,ndim):
    for surf_tag in surf_list:
                surf_id = surf_tag[1]
                com = gmsh.model.occ.getCenterOfMass(ndim - 1, surf_id)

                # print(com)
                
                _add_to_domain_markers("sur"+str(surf_id), [surf_id], "facet")
                count_surface +=1
    return count_surface

def set_length_scale(surface_id,  lcmin, lcmax, dismin, distmax ):
    distance = gmsh.model.mesh.field.add("Distance")
    gmsh.model.mesh.field.setNumbers(
        distance, "FacesList", domain_markers[surface_id]["gmsh_tags"]
    )

    threshold = gmsh.model.mesh.field.add("Threshold")
    gmsh.model.mesh.field.setNumber(threshold, "IField", distance)

    
    # half_panel = params.pv_array.panel_chord * np.cos(params.pv_array.tracker_angle)
    # gmsh.model.mesh.field.setNumber(threshold, "LcMin", resolution * 0.5)
    # resolution = factor * 10 * params.pv_array.panel_thickness / 2
    gmsh.model.mesh.field.setNumber(threshold, "LcMin", lcmin )

    gmsh.model.mesh.field.setNumber(threshold, "LcMax", lcmax)
    gmsh.model.mesh.field.setNumber(
        threshold, "DistMin", dismin
    )
    gmsh.model.mesh.field.setNumber(
        threshold, "DistMax", distmax
    )

    return threshold

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

ndim = 3
domain_markers = {}
    # Must start indexing at 1, if starting at 0, things marked "0"
    # are indistinguishable from things which receive no marking (and have default value of 0)
domain_markers["_current_idx"] = 1
count_surface = 0
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


# cut and remove the extended part of left frame
cutted_left_frame = gmsh.model.occ.fragment([(3,left_frame_tag)],[(2,cut_surface_left_front), (2,cut_surface_left_rear)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_left_frame[0][0], cutted_left_frame[0][2]], recursive=True)
# final tag of frame at left
final_left_frame_tag = cutted_left_frame[0][1][1]
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_left_frame[0])[0]):
    remove_surface_list.append(cutted_left_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)

# cut and remove the extended part of front frame
cutted_front_frame = gmsh.model.occ.fragment([(3,front_frame_tag)],[(2,cut_surface_left_front), (2,cut_surface_right_front_tag)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_front_frame[0][0], cutted_front_frame[0][2]], recursive=True)
# final tag of frame at front
final_front_frame_tag = cutted_front_frame[0][1][1]
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_front_frame[0])[0]):
    remove_surface_list.append(cutted_front_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)

# cut and remove the extended part of right frame
cutted_right_frame = gmsh.model.occ.fragment([(3,right_frame_tag)],[(2,cut_surface_right_front_tag), (2,cut_surface_right_rear_tag)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_right_frame[0][0], cutted_right_frame[0][2]], recursive=True)
# final tag of frame at right
final_right_frame_tag = cutted_right_frame[0][1][1]
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_right_frame[0])[0]):
    remove_surface_list.append(cutted_right_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)

# cut and remove the extended part of right frame
cutted_rear_frame = gmsh.model.occ.fragment([(3,rear_frame_tag)],[(2,cut_surface_right_rear_tag), (2,cut_surface_left_rear)], removeTool=False)
# remove the extended part of the frame
gmsh.model.occ.remove([cutted_rear_frame[0][0], cutted_rear_frame[0][2]], recursive=True)
# final tag of frame at rear
final_rear_frame_tag = cutted_rear_frame[0][1][1]
# remove the cutting surface
remove_surface_list = []
for i in range(3,np.shape(cutted_rear_frame[0])[0]):
    remove_surface_list.append(cutted_rear_frame[0][i])
gmsh.model.occ.remove(remove_surface_list, recursive=True)

# remove surfaces used to cut frames
gmsh.model.occ.remove([(2,cut_surface_right_rear_tag), (2,cut_surface_left_rear),(2,cut_surface_right_front_tag), (2,cut_surface_left_front) ], recursive=True)
# remove interfaces between frames, all tags of frames are not changed
gmsh.model.occ.fragment([(3, final_front_frame_tag),(3, final_rear_frame_tag)],[(3, final_left_frame_tag), (3, final_right_frame_tag)])

gmsh.model.occ.synchronize()


#               4                   
#       ===============
#       |             |
#       |             |
# y   1 |             |   3
#       |             |
#       ===============
#               2     
#               x
#    
# gmsh.model.occ.synchronize()
count_volumes=0
count_surface = 0

# # capture surfaces
# surf_tag_list = gmsh.model.occ.getEntities(ndim - 1)
# surf_list = surf_tag_list[count_surface:][:]
# count_surface =  surface_tags(surf_list,count_surface,ndim)

structure_vol_list =["frm0","frm1","frm2","frm3"]
# vol_tag_list = gmsh.model.occ.getEntities(ndim)
# vol_list = vol_tag_list[count_volumes:][:]
# count_volumes, structure_vol_list =  volume_tags(vol_list,count_volumes,structure_vol_list)

# min_dist=[]
# for volid in structure_vol_list:
#     threshold = set_length_scale(volid,  frame_thick*100, frame_thick*100, 0, 0 )#3
#     min_dist.append(threshold)


# # gmsh.model.mesh.generate(3)


# gmsh.write("panel_geo.msh")
# gmsh.write("panel_geo.vtk")

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


# gmsh.model.occ.synchronize()
gmsh.model.occ.synchronize()

# # capture surfaces
surf_tag_list = gmsh.model.occ.getEntities(ndim - 1)
surf_list = surf_tag_list[count_surface:][:]
count_surface =  surface_tags(surf_list,count_surface,ndim)

vol_tag_list = gmsh.model.occ.getEntities(ndim)
vol_list = vol_tag_list[count_volumes:][:]
structure_vol_list +=["back_sheet","back_encap","front_encap","front_glass"]

for i in range(n_cell_length):
    for j in range(n_cell_width):
        structure_vol_list.append("cell"+str(i*n_cell_width + j))

structure_vol_list.append("cell_layer_encap")
structure_vol_list.append("seal")
count_volumes, structure_vol_list =  volume_tags(vol_list,count_volumes,structure_vol_list)

from_domain_markers_to_PhysicalName(domain_markers,ndim)


min_dist = []
for volid in structure_vol_list:
    threshold = set_length_scale(volid,  frame_thick*1, frame_thick*10, 0, 0.1 )#3
    min_dist.append(threshold)

threshold = set_length_scale("back_sheet",  back_sheet_thick*10 ,back_sheet_thick*100, 0, 0.1 )#3
min_dist.append(threshold)
threshold = set_length_scale("back_encap",  back_encap_thick*10 , back_encap_thick*100, 0, 0.1 )#3
min_dist.append(threshold)
threshold = set_length_scale("front_encap",  front_encap_thick*10 , front_encap_thick*100, 0, 0.1 )#3
min_dist.append(threshold)
threshold = set_length_scale("front_glass",  front_glass_thick*10, front_glass_thick*100, 0, 0.1 )#3
min_dist.append(threshold)


for i in range(n_cell_length):
    for j in range(n_cell_width):
        threshold = set_length_scale("cell"+str(i*n_cell_width + j),  cell_thick*1, cell_thick*10, 0, .1 )#3
        min_dist.append(threshold)

threshold = set_length_scale("seal",  seal_thick*10 , seal_thick*100, 0, 0.1 )#3
min_dist.append(threshold)

minimum = gmsh.model.mesh.field.add("Min")
gmsh.model.mesh.field.setNumbers(minimum, "FieldsList", min_dist)
gmsh.model.mesh.field.setAsBackgroundMesh(minimum)


gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)     


gmsh.option.setNumber("Mesh.Algorithm", 5)
gmsh.option.setNumber("Mesh.Algorithm3D", 1)
gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 0)
gmsh.model.mesh.setOrder(1)


gmsh.model.mesh.generate(3)
gmsh.write("panel_geo.msh")
gmsh.write("panel_geo.vtk")

gmsh.finalize()
