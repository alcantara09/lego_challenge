from dataclasses import dataclass, field

@dataclass
class Colour:
    name: str
    id: int = field(default_factory=int)