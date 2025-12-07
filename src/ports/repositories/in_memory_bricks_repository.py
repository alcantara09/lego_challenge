from src.domain.entities.set import Set
from src.domain.entities.user import User
from src.domain.entities.colour import Colour
from src.domain.entities.part import Part
from src.domain.entities.inventory import Inventory
from src.ports.repositories.bricks_repository import BricksRepository

class InMemoryBricksRepository(BricksRepository):
    sets: list[Set]
    users: list[User]

    def get_all_sets(self) -> list[Set]:
        return self.sets
    
    def get_parts_by_set_id(self, set_id: int) -> dict[int, int]:
        parts = {}
        set = next((s for s in self.sets if s.id == set_id), None)
        return set.required_parts if set else parts
    
    def get_all_users(self) -> list[User]:
        return self.users
    
    def get_inventory_of_user(self, user_id: int) -> Inventory:
        user = next((u for u in self.users if u.id == user_id), None)
        return user.inventory if user else None
    
    def create_colour(self, colour: Colour) -> Colour:
        pass

    def create_user(self, user: User) -> User:
        self.users.append(user)
        return user
    
    def get_all_colours(self) -> list[Colour]:
        pass

    def get_all_parts(self) -> list[Part]:
        pass
    
