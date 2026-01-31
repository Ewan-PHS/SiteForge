# import math
from PIL import Image
import meshlib.mrcudapy
import meshlib.mrmeshnumpy
import meshlib.mrmeshpy
import meshlib.mrviewerpy
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
import cv2
import torch
import meshlib
import time
import point_cloud_utils as pcu
import os
import meshio
import argparse

# print(torch.cuda.is_available())
# print(torch.cuda.get_device_name(0))
# print(torch.__version__)
# print("CUDA available:", torch.cuda.is_available())

def filter_point_cloud_x3points(input, iterations):
    # Load your point cloud
    # pcd = o3d.io.read_point_cloud(input)  # or .xyz, .pcd, etc.
    pcd = input

    # Use DBSCAN to cluster the point cloud
    labels = np.array(pcd.cluster_dbscan(eps=0.05, min_points=1, print_progress=False))

    # Get number of clusters
    max_label = labels.max()

    # Collect only clusters with exactly 3 points
    filtered_points = []

    for i in range(max_label + 1):
        indices = np.where(labels == i)[0]
        if len(indices) == 3: #3:
            cluster_points = np.asarray(pcd.points)[indices]
            filtered_points.extend(cluster_points)

    # Create new point cloud from filtered points
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(np.vstack(filtered_points))
    return filtered_pcd


################################################################################################################
# def pixel_iterating_gpu(pixels1, pixels2, pixels3, width1, height1, width2, height2, width3, height3, r, g, b):
def pixel_iterating_gpu(width1, height1, pixels1, width2, height2, pixels2, width3, height3, pixels3, r, g, b):
    device = torch.device("cuda")

    color = torch.tensor([r, g, b], device=device)

    out = []

    # ---------- XY ----------
    p1 = torch.from_numpy(pixels1).to(device)
    mask1 = (p1 == color).all(dim=2)
    xy = torch.nonzero(mask1)

    z1 = int(((height2 + height3) / 2) + 1)
    z = torch.arange(z1, device=device)

    xy = xy.repeat(z1, 1)
    z = z.repeat_interleave(len(xy) // z1)

    out.append(torch.stack([xy[:,1], xy[:,0], z - 0], dim=1))

    # ---------- XZ ----------
    p2 = torch.from_numpy(pixels2).to(device)
    mask2 = (p2 == color).all(dim=2)
    xz = torch.nonzero(mask2)

    z2 = int(((height1 + width3) / 2) + 1)
    z = torch.arange(z2, device=device)

    xz = xz.repeat(z2, 1)
    z = z.repeat_interleave(len(xz) // z2)

    out.append(torch.stack([xz[:,1], z - 1, xz[:,0]], dim=1))

    # ---------- YZ ----------
    p3 = torch.from_numpy(pixels3).to(device)
    mask3 = (p3 == color).all(dim=2)
    yz = torch.nonzero(mask3)

    z3 = int(((width1 + width2) / 2) + 1)
    z = torch.arange(z3, device=device)

    yz = yz.repeat(z3, 1)
    z = z.repeat_interleave(len(yz) // z3)

    out.append(torch.stack([z - 1, yz[:,0], yz[:,1]], dim=1))

    output_cpu = (torch.cat(out, dim=0)).cpu()
    np_points_out = output_cpu.numpy().astype(float)
    print(np_points_out)
    return np_points_out

################################################################################################################
# def pixel_iterating(width1, height1, pixels1, width2, height2, pixels2, width3, height3, pixels3, r, g, b):
#     generated_point_set = []
    
#     # Iterate through each pixel decide whether to add it to the point set
#     # xy
#     for z in range(int(((height2 + height3) / 2) + 1)):
#         for x in range(width1):
#             for y in range(height1):
#                 r1, g1, b1 = pixels1[x, y]

#                 if r1 == r and g1 == g and b1 == b:
#                     generated_point_set.append([x, y, z - 1])

#     # xz
#     for z in range(int(((height1 + width3) / 2) + 1)):
#         for x in range(width2):
#             for y in range(height2):
#                 r2, g2, b2 = pixels2[x, y]

#                 if r2 == r and g2 == g and b2 == b:
#                     generated_point_set.append([x, z - 1, y])

#     # yz
#     for z in range(int(((width1 + width2) / 2) + 1)):
#         for x in range(width3):
#             for y in range(height3):
#                 r3, g3, b3 = pixels3[x, y]

#                 if r3 == r and g3 == g and b3 == b:
#                     generated_point_set.append([z - 1, y, x])
    
#     return generated_point_set


################################################################################################################


def x3images_to_point_cloud(img01, img02, img03):
    # Convert image to RGB mode if it's not already
    img01 = img01.convert('RGB')
    img02 = img02.convert('RGB')
    img03 = img03.convert('RGB')

    # Load the pixel data
    # pixels_1 = img01.load()
    # pixels_2 = img02.load()
    # pixels_3 = img03.load()

    # Converting pixel data to numpy arrary
    pixels_1 = np.asarray(img01, dtype=np.uint8)
    pixels_2 = np.asarray(img02, dtype=np.uint8)
    pixels_3 = np.asarray(img03, dtype=np.uint8)

    pixels01 = pixels_1.copy()
    pixels02 = pixels_2.copy()
    pixels03 = pixels_3.copy()

    # Get the width and height of the image
    width_1, height_1 = img01.size
    width_2, height_2 = img02.size
    width_3, height_3 = img03.size

    generated_point_set = []

    img_1_colours = Counter(img01.get_flattened_data())
    img_2_colours = Counter(img02.get_flattened_data())
    img_3_colours = Counter(img03.get_flattened_data())

    total_unique_colours = []

    total_unique_colours.append(list(set(img_1_colours.keys())))
    total_unique_colours.append(list(set(img_2_colours.keys())))
    total_unique_colours.append(list(set(img_3_colours.keys())))

    # total_unique_colours_set = set(total_unique_colours)

    unique_colours = list(total_unique_colours)

    if (0, 0, 0) in unique_colours[0]:
        unique_colours[0].remove((0, 0, 0))
        unique_colours[0].append((256, 256, 256))
        print("black space removed")

    print("Unique colours:")
    print(unique_colours)

    tot_colours_img_1 = img01.getcolors()
    tot_colours_img_2 = img02.getcolors()
    tot_colours_img_3 = img03.getcolors()

    repeat_iteration = max(len(tot_colours_img_1), len(tot_colours_img_2), len(tot_colours_img_3))
    print("No. iterations to go through: "+str(repeat_iteration))

    filtered_pc = o3d.geometry.PointCloud()

    for i in range(repeat_iteration):
        point_set = []
        # Create point cloud
        point_cloud = o3d.geometry.PointCloud()

        point_cloud.clear()
                                                                                                                                         #  R                        G                        B
        point_set = (pixel_iterating_gpu(height_1, width_1, pixels01, height_2, width_2, pixels02, height_3, width_3, pixels03, unique_colours[0][i][0], unique_colours[0][i][1], unique_colours[0][i][2]))
        
        print(point_set)

        # Put points into point cloud
        point_cloud.points = o3d.utility.Vector3dVector(point_set)
        if len(point_set) > 0:
            filtered_pc = filtered_pc + filter_point_cloud_x3points(point_cloud, repeat_iteration)
        else:
            filtered_pc = filtered_pc

        print("Iteration: "+str(i))
        print(unique_colours[0][i])
        print(f"{unique_colours[0][i][0]}, {unique_colours[0][i][1]}, {unique_colours[0][i][2]}")
    # generated_point_set = [list(x) for x in set(map(tuple, generated_point_set))]

################################################################################################################

    # # Create point cloud
    # point_cloud = o3d.geometry.PointCloud()

    # # Put points into point cloud
    # point_cloud.points = o3d.utility.Vector3dVector(generated_point_set)

    # # Displaying point cloud
    # # o3d.visualization.draw_geometries([point_cloud])

    # # Filtering point cloud
    # filtered_pc = filter_point_cloud_x3points(point_cloud, repeat_iteration)

    filtered_pc.remove_duplicated_points()
    print(filtered_pc)
    return filtered_pc


################################################################################################################
################################################################################################################
################################################################################################################


def select_img_1():
    file_path1 = tk.filedialog.askopenfilename(initialdir="/downloads", title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    global img_1_path
    img_1_path = file_path1


def path_1():
    # print(img_1_path)
    return img_1_path


def select_img_2():
    file_path2 = tk.filedialog.askopenfilename(initialdir="/downloads", title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    global img_2_path
    img_2_path = file_path2


def path_2():
    # print(img_2_path)
    return img_2_path


def select_img_3():
    file_path3 = tk.filedialog.askopenfilename(initialdir="/downloads", title="Select a File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    global img_3_path
    img_3_path = file_path3


def path_3():
    # print(img_3_path)
    return img_3_path


def display_point_cloud(image_1, image_2, image_3):
    # Open the image file
    img_1 = Image.open(image_1)
    img_2 = Image.open(image_2)
    img_3 = Image.open(image_3)

    pcd = x3images_to_point_cloud(img_1, img_2, img_3)

    # Add axis
    axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=2, origin=pcd.get_center())

    # display_point_cloud.pc = [pcd, axis]
    return [pcd, axis]


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


# def threading_for_gen():
#     t1 = Thread(target=save_file_path)
#     t1.start()


# def close_tkinter_window():
#     root.quit()
#     root.destroy()


# CODE STARTS HERE:

# Parser to allow for passing arguments when running the .py file
parser = argparse.ArgumentParser(description="A simple CLI tool.")
parser.add_argument("opengui", type=int, help="Int, (0=False, 1=True), whether to open built-in the GUI.")
parser.add_argument("TopViewPath", type=str, help="String, path for top-view image")
parser.add_argument("FrontViewPath", type=str, help="String, path for front-view image")
parser.add_argument("RightViewPath", type=str, help="String, path for right-view image")
parser.add_argument("Name", type=str, help="String, name of 3D model")
parser.add_argument("SavePath", type=str, default="C:\\Users\\ewanc\\Downloads", help="String, path to save the 3D model at")

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

    # button_generate = tk.Button(root, text="Generate", command=display_point_cloud(im_1, im_2, im_3))
    # button_generate.pack(pady=20)

    label = tk.Label(root, text="Path to save .stl file. E.g: C:\\Users\\<EXAMPLENAME>\\Downloads")
    label.pack(pady=0)

    file_save_path = tk.Entry(root, width=55, borderwidth=2)
    file_save_path.pack(pady=0)

    # save_path = tk.Button(root, text="Save", command=save_file_path)
    # save_path.pack(pady=0)

    label1 = tk.Label(root, text="""
    Name of .stl file""")
    label1.pack(pady=0)

    file_save_name = tk.Entry(root, width=35, borderwidth=2)
    file_save_name.pack(pady=0)

    # exit_button = tk.Button(root, text="Close and generate", command=threading_for_gen)
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

pcd_load = display_point_cloud(img_1_path, img_2_path, img_3_path)[0]

xyz_load = np.asarray(pcd_load.points)

if args.opengui == 1:
    path_to_save = file_path()
    name_to_save = file_name()

if args.opengui == 0:
    path_to_save = args.SavePath
    name_to_save = args.Name

# print(xyz_load)

# Below is code for PyVista
# # points is a 3D numpy array (n_points, 3)
# cloud = pv.PolyData(xyz_load)
# # cloud.plot()
# print("Point cloud created.")

# volume = cloud.delaunay_3d(alpha=1.)
# shell = volume.extract_geometry()
# mesh = shell.triangulate()
# # mesh.plot()

# mesh.save(f'{path_to_save}\\{name_to_save}.stl', binary=True)
# print("Mesh saved.")

# Below is code for MeshLib
points = meshlib.mrmeshnumpy.pointCloudFromPoints(xyz_load)

# Generate mesh from point cloud

# params = meshlib.mrmeshpy.TriangulationParameters()
# params.radius = 4
mesh = meshlib.mrmeshpy.triangulatePointCloud(points)#, params)

# Getting the path of Appdata/local to store tmp files. Creating folders in Appdata local for the app
appdata_local = os.getenv('LOCALAPPDATA')

SiteForge_dir = os.path.join(appdata_local, 'SiteForge')
os.makedirs(SiteForge_dir, exist_ok=True)

SiteForge_tmp_dir = os.path.join(SiteForge_dir, 'temp')
os.makedirs(SiteForge_tmp_dir, exist_ok=True)

meshlib.mrmeshpy.saveMesh(mesh, (f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply'))

v, f = pcu.load_mesh_vf(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply')

if os.path.exists(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply'):
    os.remove(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp.ply')
    print("tmp .ply deleted.")

resolution = 12500
v_watertight, f_watertight = pcu.make_mesh_watertight(v, f, resolution=resolution)

pcu.save_mesh_vf(v=v_watertight, f=f_watertight, filename=(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply'))

output_mesh = meshio.read(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply')

if os.path.exists(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply'):
    os.remove(f'{SiteForge_tmp_dir}\\{name_to_save}_tmp-final.ply')
    print("tmp-final .ply deleted.")

# To get the end time of execution
end_time = time.perf_counter()

# Save the resulting mesh
meshio.write((f'{path_to_save}\\{name_to_save}.stl'), output_mesh)

end_save_time = time.perf_counter()

print(f"""
################################################
Name: {name_to_save}
Execution time: {end_time - start_time} seconds
Save time: {end_save_time - end_time} seconds
################################################
""")

# meshlib.mrviewerpy.addMeshToScene(mesh, f"{name_to_save}.stl")
# meshlib.mrviewerpy.launch()

# # Displaying point cloud
# o3d.visualization.draw_geometries(display_point_cloud(img_1_path, img_2_path, img_3_path))
