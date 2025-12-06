from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Inventory:
    parts: dict[UUID, int] # Mapping of Part ID to quantity
    id: UUID = field(default_factory=uuid4)
