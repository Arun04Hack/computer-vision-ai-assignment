import json
from pathlib import Path

from item import Item


def load_items(file_path: str | Path) -> list[Item]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_items = json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON format.") from exc

    if not isinstance(raw_items, list):
        raise ValueError("JSON root must be a list of items.")

    items: list[Item] = []

    for index, item in enumerate(raw_items, start=1):

        if not isinstance(item, dict):
            raise ValueError(f"Item #{index} must be a JSON object.")

        required_keys = {"id", "dims", "type"}

        if not required_keys.issubset(item):
            missing = required_keys - item.keys()
            raise ValueError(f"Item #{index} is missing required keys: {missing}")

        dims = item["dims"]

        if (not isinstance(dims, list) or len(dims) != 3 or not all(isinstance(value, int) for value in dims)):
            raise ValueError(f"Item #{index} has invalid dimensions.")

        items.append(
            Item(
                id=item["id"],
                dims=tuple(dims),
                type=item["type"],
            )
        )

    return items

# def load_items(path: str) -> list[Item]:
#     try:
#         with open(path, 'r') as file:
#             raw_items = json.load(file)
#     except FileNotFoundError:
#         raise FileNotFoundError("Error! File Not Found")
#     except json.JSONDecodeError:
#         raise ValueError("Invalid JSON format.")
    
#     loaded_items = []
    
#     for item in raw_items:
#         loaded_items.append(
#             Item(
#             id = item['id'],
#             dims= tuple(item['dims']),
#             type= item['type']
#             )
#         )
        
    
#     return loaded_items