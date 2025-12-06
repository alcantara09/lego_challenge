from dataclasses import dataclass, field
from uuid import UUID, uuid4
from src.domain.entities.part import Part

@dataclass
class Set:
    name: str
    required_parts: dict[UUID, int]
    id: UUID = field(default_factory=uuid4)
