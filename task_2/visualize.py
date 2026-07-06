import time
import open3d as o3d

from item import PlacedItem

COLOR_MAP = {
    "standard_box": (0.25, 0.65, 0.95),   # Blue
    "flat_panel":   (0.95, 0.60, 0.20),   # Orange
    "long_beam":    (0.45, 0.75, 0.30),   # Green
    "large_crate":  (0.80, 0.35, 0.35),   # Red
    "medium_cube":  (0.65, 0.45, 0.85),   # Purple
    "small_filler": (0.60, 0.60, 0.60),   # Gray
    "long_box":     (0.20, 0.75, 0.75),   # Cyan
    "flat_box":     (0.95, 0.85, 0.25),   # Yellow
}

DEFAULT_COLOR = (0.70, 0.70, 0.70)


def create_box(position: tuple[int, int, int], size: tuple[int, int, int], color: tuple[float, float, float], ) -> o3d.geometry.TriangleMesh:
    box = o3d.geometry.TriangleMesh.create_box(width=size[0], height=size[1], depth=size[2], )

    box.translate(position)
    box.paint_uniform_color(color)

    return box


def create_container(container_size: tuple[int, int, int]) -> o3d.geometry.LineSet:

    width, height, depth = container_size

    points = [
        [0, 0, 0],
        [width, 0, 0],
        [width, height, 0],
        [0, height, 0],

        [0, 0, depth],
        [width, 0, depth],
        [width, height, depth],
        [0, height, depth],
    ]

    lines = [
        [0,1],[1,2],[2,3],[3,0],

        [4,5],[5,6],[6,7],[7,4],

        [0,4],[1,5],[2,6],[3,7],
    ]

    colors = [[0,0,0] for _ in lines]

    container = o3d.geometry.LineSet()

    container.points = o3d.utility.Vector3dVector(points)
    container.lines = o3d.utility.Vector2iVector(lines)
    container.colors = o3d.utility.Vector3dVector(colors)

    return container


def visualize_packing(placed_items: list[PlacedItem], container_size: tuple[int, int, int], delay: float = 0.4, ) -> None:
    vis = o3d.visualization.Visualizer()

    vis.create_window(
        window_name="3D Bin Packing",
        width=1200,
        height=900,
    )

    vis.add_geometry(create_container(container_size))

    for placed in placed_items:

        color = COLOR_MAP.get(
                placed.item.type,
                DEFAULT_COLOR,
        )

        mesh = create_box(
            position=placed.position,
            size=placed.orientation,
            color=color,
        )

        vis.add_geometry(mesh)

        vis.poll_events()
        vis.update_renderer()

        time.sleep(delay)

    vis.run()
    vis.destroy_window()