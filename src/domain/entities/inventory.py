from dataclasses import dataclass, field

@dataclass
class Inventory:
    parts: dict[int, int] # Mapping of Part ID to quantity
    id: int = field(default_factory=int)
