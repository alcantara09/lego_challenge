from dataclasses import dataclass, field
from src.domain.entities.part import Part

@dataclass
class InventoryItem:
    part: Part
    quantity: int

@dataclass
class Inventory:
    parts: list[InventoryItem] = field(default_factory=list)
    id: int = field(default_factory=int)