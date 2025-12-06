from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID
from src.domain.entities.set import Set
from src.domain.entities.user import User
from src.domain.entities.inventory import Inventory

class BricksRepository(ABC):
    @abstractmethod
    def get_all_sets(self) -> list[Set]:
        pass

    @abstractmethod
    def get_parts_by_set_id(self, set_id: UUID) -> dict[int, int]:
        pass
    
    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass
    
    @abstractmethod
    def get_inventory_of_user(self, user_id: UUID) -> Inventory:
        pass

    @abstractmethod
    def create_colour(self, colour: Any) -> Any:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_all_colours(self) -> list[Any]:
        pass