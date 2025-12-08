from dataclasses import dataclass, field
from src.domain.entities.part import Part

@dataclass
class SetItem:
    part: Part
    quantity: int

@dataclass
class Set:
    name: str
    parts: list[SetItem] = field(default_factory=list)
    id: int = field(default_factory=int)
