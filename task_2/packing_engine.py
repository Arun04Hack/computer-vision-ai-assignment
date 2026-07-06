from item import Item, PlacedItem


class PackingEngine:

    def __init__(self, container_size: tuple[int, int, int], items: list[Item]):

        self.container_size = container_size
        self.items = items.copy()
        self.placed_items: list[PlacedItem] = []
        self.candidate_positions: list[tuple[int, int, int]] = [(0, 0, 0)]

    def check_boundary(self, position: tuple[int, int, int], orientation: tuple[int, int, int]) -> bool:

        x, y, z = position
        dx, dy, dz = orientation

        cx, cy, cz = self.container_size

        return (
            x >= 0
            and y >= 0
            and z >= 0
            and x + dx <= cx
            and y + dy <= cy
            and z + dz <= cz
        )

    def check_collision(self, position: tuple[int, int, int], orientation: tuple[int, int, int]) -> bool:

        x1, y1, z1 = position
        dx1, dy1, dz1 = orientation

        x2 = x1 + dx1
        y2 = y1 + dy1
        z2 = z1 + dz1

        for placed in self.placed_items:

            px, py, pz = placed.position

            pdx, pdy, pdz = placed.orientation

            px2 = px + pdx
            py2 = py + pdy
            pz2 = pz + pdz

            overlap_x = (x1 < px2 and x2 > px)

            overlap_y = (y1 < py2 and y2 > py)

            overlap_z = (z1 < pz2 and z2 > pz)

            if overlap_x and overlap_y and overlap_z:
                return True

        return False
    
    def check_support(self, position: tuple[int, int, int], orientation: tuple[int, int, int]) -> bool:
        x, y, z = position
        dx, dy, dz = orientation

        if z == 0:
            return True

        for placed in self.placed_items:

            px, py, pz = placed.position
            pdx, pdy, pdz = placed.orientation

            top_surface = pz + pdz

            if top_surface != z:
                continue

            overlap_x = (x < px + pdx and x + dx > px)

            overlap_y = (y < py + pdy and y + dy > py)

            if overlap_x and overlap_y:
                    return True

        return False

    def update_candidate_positions(self, placed_item: PlacedItem) -> None:
        x, y, z = placed_item.position
        dx, dy, dz = placed_item.orientation

        candidates = [(x + dx, y, z), (x, y + dy, z), (x, y, z + dz), ]

        for candidate in candidates:

            if candidate not in self.candidate_positions:
                self.candidate_positions.append(candidate)
                
    def place_item(self, item: Item, orientations: list[tuple[int, int, int]]) -> bool:
        self.candidate_positions.sort(key=lambda p: (p[2], p[1], p[0]))

        for orientation in orientations:

            for position in self.candidate_positions:

                if not self.check_boundary(position, orientation):
                    continue

                if self.check_collision( position, orientation):
                    continue

                if not self.check_support( position, orientation):
                    continue

                placed_item = PlacedItem(item=item, position=position, orientation=orientation)

                self.placed_items.append(placed_item)

                self.update_candidate_positions(placed_item)

                self.candidate_positions.remove(position)

                return True

        return False
    
    def pack(self) -> list[PlacedItem]:
        # Larger base first.
        self.items.sort(
            key=lambda item: (
                -(max(item.dims) * sorted(item.dims)[1]),
                -(item.dims[0] * item.dims[1] * item.dims[2])
            )
        )

        from orientation import generate_unique_orientations

        for item in self.items:

            orientations = generate_unique_orientations(item)

            packed = self.place_item(item, orientations)

            if not packed:

                print(
                    f"Warning: "
                    f"Item {item.id} "
                    f"could not be packed."
                )

        return self.placed_items