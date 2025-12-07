from dataclasses import dataclass, field

@dataclass
class Shape:
    name: str
    id: int = field(default_factory=int)
