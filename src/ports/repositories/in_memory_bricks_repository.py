from src.domain.entities.set import Set
from src.domain.entities.user import User
from src.domain.entities.colour import Colour
from src.domain.entities.part import Part
from src.domain.entities.inventory import Inventory
from src.domain.entities.set import SetItem
from src.ports.repositories.bricks_repository import BricksRepository

class InMemoryBricksRepository(BricksRepository):
    sets: list[Set]
    users: list[User]

    def get_all_sets(self) -> list[Set]:
        return self.sets
    
    def get_parts_by_set_id(self, set_id: int) -> list[SetItem]:
        lego_set = next((s for s in self.sets if s.id == set_id), None)
        return lego_set.parts if lego_set else []
    
    def get_set_by_id(self, set_id: int) -> Set:
        return next((s for s in self.sets if s.id == set_id), None)
    
    def get_set_by_name(self, name: str) -> Set:
        return next((s for s in self.sets if s.name == name), None)
    
    def create_colour(self, colour: Colour) -> Colour:
        pass

    def create_user(self, user: User) -> User:
        self.users.append(user)
        return user
    
    def get_user_by_id(self, user_id: int) -> User:
        return next((u for u in self.users if u.id == user_id), None)

    def get_user_by_name(self, name: str) -> User:
        return next((u for u in self.users if u.name == name), None)
    
    def get_all_users(self) -> list[User]:
        return self.users
    
    def get_all_colours(self) -> list[Colour]:
        pass

    def get_all_parts(self) -> list[Part]:
        pass

    def get_inventory_by_id(self, inventory_id: int) -> Inventory:
        return
    
