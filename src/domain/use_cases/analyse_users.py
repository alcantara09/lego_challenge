from src.domain.entities.inventory import Inventory
from src.domain.entities.user import User
from uuid import UUID
from src.ports.repositories.bricks_repository import BricksRepository

class AnalyseUsers:
    def __init__(self, bricks_repository: BricksRepository):
        self.bricks_repository = bricks_repository

    def retrieve_other_users_with_parts(self, current_user: User, inventory: Inventory) -> dict[UUID, int]:
        all_users = self.bricks_repository.get_all_users()
        users_with_parts = {}
        for user in all_users:
            if user.id == current_user.id:
                continue
            user_inventory = self.bricks_repository.get_inventory_of_user(user.id)
            number_of_common_parts = len(set(user_inventory.parts.keys()) & set(inventory.parts.keys()))
            if number_of_common_parts > 0:
                users_with_parts[user.id] = number_of_common_parts
        return dict(sorted(users_with_parts.items(), key=lambda x: x[1], reverse=True))
    