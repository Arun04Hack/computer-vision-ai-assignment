# import open3d as o3d
# import numpy as np



# mesh = o3d.io.read_triangle_mesh("data/TEAPOT.obj")

# minimal_obb = mesh.get_minimal_oriented_bounding_box()
# # minimal_obb = mesh.get_oriented_bounding_box()
# minimal_obb.color = (1, 0, 0)

# #Create a visualizer
# vis = o3d.visualization.Visualizer()
# vis.create_window()

# vis.add_geometry(mesh)
# vis.add_geometry(minimal_obb)

# vis.run()

# vis.destroy_window()

# print(type(minimal_obb))
# print(minimal_obb.extent)
# print(minimal_obb.volume())
# print(minimal_obb.center)
# print(minimal_obb.R)

import os
import sys

import open3d as o3d


RED = (1, 0, 0)
BLUE = (0, 0, 1)


def load_mesh(path):
    mesh = o3d.io.read_triangle_mesh(path)

    if mesh.is_empty():
        raise ValueError(f"Unable to load mesh: {path}")

    return mesh


def compute_minimum_obb(mesh):
    obb = mesh.get_minimal_oriented_bounding_box()
    obb.color = RED
    return obb


def compute_pca_obb(mesh):
    obb = mesh.get_oriented_bounding_box()
    obb.color = BLUE
    return obb


def format_dimensions(extent):
    return f"{extent[0]:.4f} x {extent[1]:.4f} x {extent[2]:.4f}"


def print_default_report(filename, obb):
    print("-" * 60)
    print(f"Object : {filename}")
    print("-" * 60)

    print("\nMinimum Oriented Bounding Box")
    print(f"Dimensions : {format_dimensions(obb.extent)}")
    print(f"Volume     : {obb.volume():.6f}")
    print()


def print_comparison_report(filename, pca_obb, minimal_obb):
    pca_volume = pca_obb.volume()
    minimal_volume = minimal_obb.volume()

    reduction = (
        (pca_volume - minimal_volume) / pca_volume * 100
        if pca_volume > 0
        else 0
    )

    print("-" * 60)
    print(f"Object : {filename}")
    print("-" * 60)

    print("\nPCA Oriented Bounding Box")
    print(f"Dimensions : {format_dimensions(pca_obb.extent)}")
    print(f"Volume     : {pca_volume:.6f}")

    print("\nMinimum Oriented Bounding Box")
    print(f"Dimensions : {format_dimensions(minimal_obb.extent)}")
    print(f"Volume     : {minimal_volume:.6f}")

    print("\nComparison")
    print(f"Volume Reduction : {reduction:.2f}%")
    print("Selected Algorithm : Minimum Oriented Bounding Box")
    print()


def visualize(mesh, *geometries):
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    vis.add_geometry(mesh)

    for geometry in geometries:
        vis.add_geometry(geometry)

    vis.run()
    vis.destroy_window()


def process_mesh(path, compare=False, visualize_result=False):
    mesh = load_mesh(path)

    minimal_obb = compute_minimum_obb(mesh)

    if compare:
        pca_obb = compute_pca_obb(mesh)
        print_comparison_report(
            os.path.basename(path),
            pca_obb,
            minimal_obb
        )

        if visualize_result:
            visualize(mesh, minimal_obb, pca_obb)

    else:
        print_default_report(
            os.path.basename(path),
            minimal_obb
        )

        if visualize_result:
            visualize(mesh, minimal_obb)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python main.py <obj1> [obj2] ... [--compare] [--visualize]")
        sys.exit(1)

    compare = False
    visualize_result = False
    mesh_paths = []

    for arg in sys.argv[1:]:
        if arg in ("-c", "--compare"):
            compare = True

        elif arg in ("-v", "--visualize"):
            visualize_result = True

        else:
            mesh_paths.append(arg)

    if not mesh_paths:
        print("No OBJ files provided.")
        sys.exit(1)

    for path in mesh_paths:
        try:
            process_mesh(
                path,
                compare,
                visualize_result
            )

        except Exception as e:
            print(f"Error processing '{path}': {e}")


if __name__ == "__main__":
    main()
    
