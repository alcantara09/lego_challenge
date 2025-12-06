from uuid import UUID

from src.domain.entities.set import Set
from src.domain.entities.user import User
from src.domain.entities.inventory import Inventory
from src.ports.repositories.bricks_repository import BricksRepository

class InMemoryBricksRepository(BricksRepository):
    sets: list[Set]
    users: list[User]

    def get_all_sets(self) -> list[Set]:
        return self.sets
    
    def get_parts_by_set_id(self, set_id: UUID) -> dict[UUID, int]:
        parts = {}
        set = next((s for s in self.sets if s.id == set_id), None)
        return set.required_parts if set else parts
    
    def get_all_users(self) -> list[User]:
        return self.users
    
    def get_inventory_of_user(self, user_id: UUID) -> Inventory:
        user = next((u for u in self.users if u.id == user_id), None)
        return user.inventory if user else None
    
    def create_colour(self, colour: Any) -> Any:
        pass

    def create_user(self, user: User) -> User:
        self.users.append(user)
        return user
    
    def get_all_colours(self) -> list[Any]:
        pass
    
