### Imports ###
# import math
import sys

from ast import arg

from PIL import Image
# import meshlib.mrcudapy
import meshlib.mrmeshnumpy
import meshlib.mrmeshpy
# import meshlib.mrviewerpy
import open3d as o3d
import numpy as np
import pyvista as pv
import tkinter as tk
from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import asksaveasfilename
# from tkinter import ttk
tk.Tk().withdraw()  # part of the import, goes at end
from threading import *
from collections import defaultdict
from collections import Counter
import torch
import meshlib
import time
import point_cloud_utils as pcu
import os
import meshio
import argparse


################################################################################################################
# Current function used to filter the pixels by colour
# Much faster as is run on the GPU

def pixel_iterating_gpu(width1, height1, pixels1, width2, height2, pixels2, width3, height3, pixels3, r, g, b):
    device = torch.device("cuda")

    color = torch.tensor([r, g, b], device=device)

    outXY = []
    outXZ = []
    outYZ = []

    # ---------- XY ----------
    p1 = torch.from_numpy(pixels1).to(device)
    mask1 = (p1 == color).all(dim=2)
    xy = torch.nonzero(mask1)

    z1 = int(((height2 + height3) / 2) + 1)
    z = torch.arange(z1, device=device)

    xy = xy.repeat(z1, 1)
    z = z.repeat_interleave(len(xy) // z1)

    outXY.append((torch.stack([xy[:,1], xy[:,0], z - 0], dim=1)).cpu())

    # p1 = torch.from_numpy(pixels1).to(device)
    # mask1 = (p1 == color).all(dim=2)
    # xy = torch.nonzero(mask1).cpu().numpy()

    # xy_set = set(map(tuple, xy[:, [1,0]]))  # (x,y)

    # ---------- XZ ----------
    p2 = torch.from_numpy(pixels2).to(device)
    mask2 = (p2 == color).all(dim=2)
    xz = torch.nonzero(mask2)

    z2 = int(((height1 + width3) / 2) + 1)
    z = torch.arange(z2, device=device)

    xz = xz.repeat(z2, 1)
    z = z.repeat_interleave(len(xz) // z2)

    outXZ.append((torch.stack([xz[:,1], z - 1, xz[:,0]], dim=1)).cpu())

    # p2 = torch.from_numpy(pixels2).to(device)
    # mask2 = (p2 == color).all(dim=2)
    # xz = torch.nonzero(mask2).cpu().numpy()

    # xz_set = set(map(tuple, xz[:, [1,0]]))  # (x,z)

    # ---------- YZ ----------
    p3 = torch.from_numpy(pixels3).to(device)
    mask3 = (p3 == color).all(dim=2)
    yz = torch.nonzero(mask3)

    z3 = int(((width1 + width2) / 2) + 1)
    z = torch.arange(z3, device=device)

    yz = yz.repeat(z3, 1)
    z = z.repeat_interleave(len(yz) // z3)

    outYZ.append((torch.stack([z - 1, yz[:,0], yz[:,1]], dim=1)).cpu())

    # p3 = torch.from_numpy(pixels3).to(device)
    # mask3 = (p3 == color).all(dim=2)
    # yz = torch.nonzero(mask3).cpu().numpy()

    # yz_set = set(map(tuple, yz[:, [0,1]]))  # (y,z)

    # print(f"""
    #       XY:{outXY[0].tolist()}
    #       XZ:{outXZ[0].tolist()}
    #       YZ:{outYZ[0].tolist()}
    # """)

    # SOT => Set Of Tuples
    outXY_SOT = set(map(tuple, outXY[0].numpy()))
    outXZ_SOT = set(map(tuple, outXZ[0].numpy()))
    outYZ_SOT = set(map(tuple, outYZ[0].numpy()))

    # points = set()
    # z1 = int(((height2 + height3) / 2) + 1)

    # for x,y in xy_set:
    #     for z in range(z1):
    #         if (x,z) in xz_set and (y,z) in yz_set:
    #             points.add((x,y,z))

    out_intersected = outXY_SOT & outXZ_SOT & outYZ_SOT
    # out_intersected = set.intersection(outXY_LOT, outXZ_LOT, outYZ_LOT)
    # print(f"out_intersected: {out_intersected}")

    return out_intersected


################################################################################################################


def x3images_to_point_cloud(img01, img02, img03):
    # Convert image to RGB mode if it's not already
    img01 = img01.convert('RGB')
    img02 = img02.convert('RGB')
    img03 = img03.convert('RGB')

    # Converting pixel data to numpy arrary
    pixels_1 = np.asarray(img01, dtype=np.uint8)
    pixels_2 = np.asarray(img02, dtype=np.uint8)
    pixels_3 = np.asarray(img03, dtype=np.uint8)

    # Creates duplicate of pixel data to allow it to be editable by the code
    pixels01 = pixels_1.copy()
    pixels02 = pixels_2.copy()
    pixels03 = pixels_3.copy()

    # Get the width and height of the image
    width_1, height_1 = img01.size
    width_2, height_2 = img02.size
    width_3, height_3 = img03.size

    # Keep the size of the images used to display as data at the end
    global Image_Size 
    Image_Size = f"{width_1} x {height_1}"

    # Get the pixel data, e.g. (R, G, B)
    img_1_colours = Counter(img01.get_flattened_data())
    img_2_colours = Counter(img02.get_flattened_data())
    img_3_colours = Counter(img03.get_flattened_data())

    # Create an array to store a list of the unique colours
    total_unique_colours = []

    # Adding the unique colours from each image the the array
    total_unique_colours.append(list(set(img_1_colours.keys())))
    total_unique_colours.append(list(set(img_2_colours.keys())))
    total_unique_colours.append(list(set(img_3_colours.keys())))

    unique_colours = list(total_unique_colours)

    # Removes black as a colour as it represents empty space, it is then replaced by a non-existant colour
    if (0, 0, 0) in unique_colours[0]:
        unique_colours[0].remove((0, 0, 0))
        unique_colours[0].append((256, 256, 256))
        # print("black space removed")

    # Code for debugging
    # print("Unique colours:")
    # print(unique_colours)

    tot_colours_img_1 = img01.getcolors()
    tot_colours_img_2 = img02.getcolors()
    tot_colours_img_3 = img03.getcolors()

    repeat_iteration = max(len(tot_colours_img_1), len(tot_colours_img_2), len(tot_colours_img_3))

    # Code for debugging
    # print("No. iterations to go through: "+str(repeat_iteration))

    intersected_set = set()

    for i in range(repeat_iteration):
        point_set = set()

        point_set.clear()
                                                                                                                                         #  R                        G                        B
        point_set = (pixel_iterating_gpu(height_1, width_1, pixels01, height_2, width_2, pixels02, height_3, width_3, pixels03, unique_colours[0][i][0], unique_colours[0][i][1], unique_colours[0][i][2]))
        
        # Code for debugging
        # print(point_set)

        if len(point_set) > 0:
            intersected_set = intersected_set.union(point_set)
        else:
            ...

    return intersected_set


################################################################################################################


def select_img_1():
    file_path1 = tk.filedialog.askopenfilename(initialdir="/downloads", title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    global img_1_path
    img_1_path = file_path1


def path_1():
    # Code for debugging
    # print(img_1_path)

    return img_1_path


def select_img_2():
    file_path2 = tk.filedialog.askopenfilename(initialdir="/downloads", title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    global img_2_path
    img_2_path = file_path2


def path_2():
    # Code for debugging
    # print(img_2_path)

    return img_2_path


def select_img_3():
    file_path3 = tk.filedialog.askopenfilename(initialdir="/downloads", title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    global img_3_path
    img_3_path = file_path3


def path_3():
    # Code for debugging
    # print(img_3_path)

    return img_3_path


def display_point_cloud(image_1, image_2, image_3):
    # Open the image file
    img_1 = Image.open(image_1)
    img_2 = Image.open(image_2)
    img_3 = Image.open(image_3)

    pcd = x3images_to_point_cloud(img_1, img_2, img_3)

    return [pcd]


def save_file_path():
    text = file_save_path.get()
    global file_path_saved
    file_path_saved = text
    save_file_name()
    root.quit()


def file_path():
    return file_path_saved


def save_file_name():
    text = file_save_name.get()
    global file_name_saved
    file_name_saved = text


def file_name():
    return file_name_saved


# CODE STARTS HERE:

# Parser to allow for passing arguments when running the .py file through cmd
parser = argparse.ArgumentParser(description="A simple CLI tool.")

parser.add_argument("opengui", type=int, help="Int, (0=False, 1=True), whether to open built-in the GUI.")

group_openGuiT = parser.add_argument_group()
group_openGuiT.add_argument("-TopViewPath", type=str, help="String, path for top-view image")
group_openGuiT.add_argument("-FrontViewPath", type=str, help="String, path for front-view image")
group_openGuiT.add_argument("-RightViewPath", type=str, help="String, path for right-view image")
group_openGuiT.add_argument("-Name", type=str, help="String, name of 3D model")
group_openGuiT.add_argument("-SavePath", type=str, default="C:\\Users\\ewanc\\Downloads", help="String, path to save the 3D model at")

args = parser.parse_args()

if args.opengui == 1:
    # Opens a tkinter GUI
    root = tk.Tk()  # creates window
    root.title("Image to 3D model")  # window title
    root.geometry("450x350")  # window size
    root.resizable(False, False)  # makes window non-resizable
    # root.iconbitmap("resources\icons\IMG_to_stl.ico")  # gives the window a custom icon

    button_img_1 = tk.Button(root, text="Select Image 1, side", command=select_img_1)
    button_img_1.pack(pady=20)

    button_img_2 = tk.Button(root, text="Select Image 2, top", command=select_img_2)
    button_img_2.pack(pady=0)

    button_img_3 = tk.Button(root, text="Select Image 3, front", command=select_img_3)
    button_img_3.pack(pady=20)

    label = tk.Label(root, text="Path to save .stl file. E.g: C:\\Users\\<EXAMPLENAME>\\Downloads")
    label.pack(pady=0)

    file_save_path = tk.Entry(root, width=55, borderwidth=2)
    file_save_path.pack(pady=0)

    label1 = tk.Label(root, text="""
    Name of .stl file""")
    label1.pack(pady=0)

    file_save_name = tk.Entry(root, width=35, borderwidth=2)
    file_save_name.pack(pady=0)

    exit_button = tk.Button(root, text="Close and generate", command=save_file_path)
    exit_button.pack(pady=20)

    root.mainloop()

    root.destroy()

if args.opengui == 0:
    img_1_path = args.RightViewPath
    img_2_path = args.TopViewPath
    img_3_path = args.FrontViewPath

# To get start time of execution
start_time = time.perf_counter()

pcd_load = list(display_point_cloud(img_1_path, img_2_path, img_3_path)[0])     # Convert the set to a list
pcd_load = [list(elem) for elem in pcd_load]        # Convert the tuples that are contained within the list into lists
# print(f"pcd_load: {pcd_load}")

xyz_load = np.asarray(pcd_load).astype(float)
# print(xyz_load.shape)

# Checks where to get the name and path from, depending on the enabled/disabled state of the GUI
if args.opengui == 1:
    path_to_save = file_path()
    path_to_save = "C:\\Users\\ewanc\\Downloads"   # to save me from typing it out every time
    name_to_save = file_name()

if args.opengui == 0:
    path_to_save = args.SavePath
    name_to_save = args.Name


# Below is code for MeshLib
points = meshlib.mrmeshnumpy.pointCloudFromPoints(xyz_load)

# Generate mesh from point cloud
# Unneeded parameters
# params = meshlib.mrmeshpy.TriangulationParameters()
# params.radius = 4
mesh = meshlib.mrmeshpy.triangulatePointCloud(points)#, params)

# Getting the path of Appdata/local to store tmp files. Creating folders in Appdata local for the app
appdata_local = os.getenv('LOCALAPPDATA')

# Creating folders for the app
SiteForge_dir = os.path.join(appdata_local, 'SiteForge')
os.makedirs(SiteForge_dir, exist_ok=True)

SiteForge_tmp_dir = os.path.join(SiteForge_dir, 'temp')
os.makedirs(SiteForge_tmp_dir, exist_ok=True)

SiteForge_render_dir = os.path.join(SiteForge_dir, 'renders')
os.makedirs(SiteForge_render_dir, exist_ok=True)

# Temporarliy saving the mesh a .ply
meshlib.mrmeshpy.saveMesh(mesh, (f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply'))

# Loading the mesh
v, f = pcu.load_mesh_vf(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply')

# Deleting temporary .ply mesh
if os.path.exists(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply'):
    os.remove(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply')
    if args.opengui == 1:
        print("tmp .ply deleted.")

# Setting the parameter for making the mesh 'watertight' / have no holes
resolution = 12500
v_watertight, f_watertight = pcu.make_mesh_watertight(v, f, resolution=resolution)

# Temporarliy saving the mesh a .ply
pcu.save_mesh_vf(v=v_watertight, f=f_watertight, filename=(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply'))

# Loading the mesh
output_mesh = meshio.read(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply')

# Deleting temporary .ply mesh
if os.path.exists(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply'):
    os.remove(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply')
    if args.opengui == 1:
        print("tmp-final .ply deleted.")

# To get the end time of execution
end_time = time.perf_counter()

# Save the resulting mesh as a .stl
meshio.write((f'{path_to_save}\\{name_to_save}.stl'), output_mesh)

# Get the time of save
end_save_time = time.perf_counter()

# Setup the rendering window
render = o3d.visualization.Visualizer()
render.create_window(width=321, height=321, visible=False) 

# Loading and importing the mesh to the window and calculating it's normals
mesh_to_render = o3d.io.read_triangle_mesh(f'{path_to_save}\\{name_to_save}.stl')
mesh_to_render.compute_vertex_normals()
mesh_to_render.compute_triangle_normals()
render.add_geometry(mesh_to_render)

# Scaling the mesh
ctr = render.get_view_control()
bbox = mesh_to_render.get_axis_aligned_bounding_box()
center = bbox.get_center()
extent = np.linalg.norm(bbox.get_extent())
mesh_to_render.scale(0.95, center=bbox.get_center())

# Setting the camera angle, position and zoom
ctr.set_lookat(center)
ctr.set_front([-1, -1, -1])  # camera direction
ctr.set_up([0, -1, 0])
ctr.set_zoom(1)

# Setting background and mesh colour
opt = render.get_render_option()
opt.background_color = np.array([0, 0, 0])   # R, G, B
opt.mesh_show_back_face = True
opt.light_on = True
opt.mesh_color_option = o3d.visualization.MeshColorOption.Default

render.poll_events()
render.update_renderer()

# Render and save the image of the mesh
image = render.capture_screen_image(f'{SiteForge_render_dir}\\rendered_{name_to_save}.png', do_render=True)
# Close the rendering window
render.destroy_window()

# Get time of the render ending
end_render_time = time.perf_counter()

if args.opengui == 1:
    # Printing telementry data for testing
    print(f"""
    ################################################
    Name: {name_to_save}
    Image Size: {Image_Size} pixels
    Execution time: {end_time - start_time} seconds
    Save time: {end_save_time - end_time} seconds
    Render time: {end_render_time - end_save_time} seconds
    ################################################
    """)

    print(f"Python Version: {sys.version}")
