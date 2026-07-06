from dataclasses import dataclass

#Dataclass is used because the class Item is just used to store the information/data from the json file. It's(class Item) a data model
@dataclass(frozen=True)
class Item:
    id: int
    dims: tuple[int, int, int]
    type: str
    
@dataclass(frozen=True)
class PlacedItem:
    item: Item
    position: tuple[int, int, int]
    orientation: tuple[int, int, int]


