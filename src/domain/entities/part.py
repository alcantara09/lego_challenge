from dataclasses import dataclass, field
from src.domain.entities.colour import Colour
from src.domain.entities.shape import Shape

@dataclass
class Part:
    material_id: str
    id: int = field(default_factory=int)