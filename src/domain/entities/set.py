from dataclasses import dataclass, field
from src.domain.entities.part import Part

from uuid import uuid4, UUID

@dataclass
class SetItem:
    part: Part
    quantity: int

@dataclass
class Set:
    name: str
    totalPieces: int 
    parts: list[SetItem] = field(default_factory=list)
    id: str | None = field(default_factory=uuid4)
