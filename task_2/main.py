# import sys
# import json
# from itertools import permutations
# from item import Item
# def main():
#     if len(sys.argv) < 2:
#         print("Usage:")
#         print("python file_name.py file_name.json")
#         sys.exit(1) 
#     items = load_items(sys.argv[1])
#     for item in items:
#         orientations = generate_unique_orientations(item)
#         print(orientations)   

# if __name__ == '__main__':
#     main()


import sys

from loader import load_items
from packing_engine import PackingEngine
from visualize import visualize_packing


MASTER_BOX = (100, 100, 100)


def print_results(engine: PackingEngine) -> None:

    print("\n" + "-" * 70)
    print("PACKING RESULTS")
    print("-" * 70)

    for placed in engine.placed_items:

        print(
            f"Item {placed.item.id:>2}"
            f" | {placed.item.type:<15}"
            f" | Position = {placed.position}"
            f" | Orientation = {placed.orientation}"
        )

    print("\n" + "-" * 70)
    print("SUMMARY")
    print("-" * 70)

    print(f"Packed Items   : {len(engine.placed_items)}")
    print(f"Unpacked Items : {len(engine.items) - len(engine.placed_items)}")

    total_volume = 0

    for placed in engine.placed_items:
        dx, dy, dz = placed.orientation
        total_volume += dx * dy * dz

    container_volume = (MASTER_BOX[0] * MASTER_BOX[1] * MASTER_BOX[2])

    utilization = (total_volume / container_volume) * 100

    print(f"Packed Volume  : {total_volume}")
    print(f"Container Size : {container_volume}")
    print(f"Utilization    : {utilization:.2f}%")

    print("-" * 70)


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py Item_List.json")
        sys.exit(1)

    items = load_items(sys.argv[1])

    engine = PackingEngine(container_size=MASTER_BOX, items=items, )

    engine.pack()

    print_results(engine)

    visualize_packing(placed_items=engine.placed_items,container_size=MASTER_BOX, )


if __name__ == "__main__":
    main()