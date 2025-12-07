from dataclasses import dataclass, field
from src.domain.entities.part import Part

@dataclass
class Set:
    name: str
    required_parts: dict[int, int]
    id: int = field(default_factory=int)
