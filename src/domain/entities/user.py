from dataclasses import dataclass, field    
from src.domain.entities.inventory import Inventory

@dataclass
class User:
    name: str
    brick_count: int
    inventory: Inventory
    id: int = field(default_factory=int)
