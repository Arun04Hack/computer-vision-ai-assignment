from itertools import permutations

from item import Item

# def generate_unique_orientations(item: Item) -> list[tuple[int, int, int]]:
    
#     return list(sorted(set(permutations(item.dims))))

def generate_unique_orientations(item: Item, ) -> list[tuple[int, int, int]]:  

    orientations = {tuple(orientation) for orientation in permutations(item.dims)}

    return sorted(orientations,
        key=lambda o: (
            o[2],            # Lowest height first
            -(o[0] * o[1])   # Largest footprint first
        )
    )