from dataclasses import dataclass, field    
from uuid import UUID, uuid4
from src.domain.entities.inventory import Inventory

@dataclass
class User:
    name: str
    inventory: Inventory
    id: UUID = field(default_factory=uuid4)
