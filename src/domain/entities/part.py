from dataclasses import dataclass, field
from src.domain.entities.colour import Colour
from src.domain.entities.shape import Shape

@dataclass
class Part:
    name: str
    shape: Shape
    colour: Colour
    id: int = field(default_factory=int)