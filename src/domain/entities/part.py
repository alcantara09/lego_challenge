from dataclasses import dataclass, field
from uuid import UUID, uuid4
from src.domain.entities.colour import Colour
from src.domain.entities.shape import Shape

@dataclass
class Part:
    name: str
    shape: Shape
    colour: Colour
    id: UUID = field(default_factory=uuid4)