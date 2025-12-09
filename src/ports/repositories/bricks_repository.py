from abc import ABC, abstractmethod
from typing import Any
from src.domain.entities.set import Set
from src.domain.entities.user import User
from src.domain.entities.inventory import Inventory
from src.domain.entities.part import Part
from src.domain.entities.colour import Colour

class BricksRepository(ABC):
    @abstractmethod
    def create_colour(self, colour: Colour) -> Colour:
        pass

    @abstractmethod
    def get_all_sets(self) -> list[Set]:
        pass

    @abstractmethod
    def get_parts_by_set_id(self, set_id: int) -> dict[int, int]:
        pass

    @abstractmethod
    def get_set_by_id(self, set_id: int) -> Set:
        pass

    @abstractmethod
    def get_set_by_name(self, name: str) -> Set:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass
    
    @abstractmethod
    def get_user_by_name(self, name: str) -> User:
        pass
    
    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_all_colours(self) -> list[Colour]:
        pass

    @abstractmethod
    def get_all_parts(self) -> list[Part]:
        pass