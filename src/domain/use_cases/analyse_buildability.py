from src.domain.entities.inventory import Inventory
from src.domain.entities.set import Set
from src.domain.entities.user import User

from src.ports.repositories.bricks_repository import BricksRepository

class AnalyseBuildability:
    def __init__(self, bricks_repository: BricksRepository):
        self.bricks_repository = bricks_repository

    def get_possible_sets_for_user_inventory(self, user_id: int) -> list[Set]:
        user = self.bricks_repository.get_user_by_id(user_id)
        inventory = self.bricks_repository.get_inventory_by_id(user.inventory.id)
        return self.get_possible_sets_from_inventory(inventory)

    def get_possible_sets_from_inventory(self, inventory: Inventory) -> list[Set]:
        all_sets = self.bricks_repository.get_all_sets()
        possible_sets = []
        for target_set in all_sets:
            required_parts = self.bricks_repository.get_parts_by_set_id(target_set.id)
            if all(inventory.parts.get(part, 0) >= qty for part, qty in required_parts.items()):
                possible_sets.append(target_set)
        return possible_sets
    
    def get_missing_parts_for_set(self, inventory: Inventory, target_set: Set) -> dict:
        required_parts = self.bricks_repository.get_parts_by_set_id(target_set.id)
        missing_parts = {}
        for part_id, qty in required_parts.items():
            available_qty = inventory.parts.get(part_id, 0)
            if available_qty < qty:
                missing_parts[part_id] = qty - available_qty
        return missing_parts
    
    def get_other_users_with_common_parts(self, users: list[User], current_user: User | None, missing_parts: dict[int, int]) -> dict[int, int]:
        all_users = users
        users_with_parts = {}
        for user in all_users:
            if current_user is not None and user.id == current_user.id:
                 continue
            user_inventory = user.inventory
            number_of_common_parts = len(set(user_inventory.parts.keys()) & set(missing_parts.keys()))
            if number_of_common_parts > 0:
                users_with_parts[user.id] = number_of_common_parts
        return dict(sorted(users_with_parts.items(), key=lambda x: x[1], reverse=True))
    
    def get_other_users_with_part(self, users: list[User], part_id: int) -> dict[int, int]:
        all_users = users
        users_with_parts = {}
        for user in all_users:
            if user.inventory.parts.get(part_id, 0) > 0:
                number_of_parts = user.inventory.parts.get(part_id, 0)
                if number_of_parts > 0:
                    users_with_parts[user.id] = number_of_parts
        return dict(sorted(users_with_parts.items(), key=lambda x: x[1], reverse=True))
    
    def suggest_users_for_part_sharing(self, current_user: User, desired_set_id: Set) -> dict[int, int]:
        inventory = self.bricks_repository.get_inventory_by_id(current_user.inventory.id)
        desired_set = self.bricks_repository.get_set_by_id(desired_set_id)
        missing_parts = self.get_missing_parts_for_set(inventory, desired_set)
        all_users = self.bricks_repository.get_all_users()
        return self.get_other_users_with_common_parts(all_users, current_user, missing_parts)
    
    def get_parts_with_percentage_of_usage(self, percentage: float) -> dict:
        all_users = self.bricks_repository.get_all_users()
        all_parts = self.bricks_repository.get_all_parts()
        parts_with_usage_above_percentage = {}

        for part in all_parts:
            users_with_part = self.get_other_users_with_part(all_users, part.id)
            if len(users_with_part) / len(all_users) >= percentage:
                number_of_parts = min(users_with_part.values())
                parts_with_usage_above_percentage[part.id] = number_of_parts
        
        return parts_with_usage_above_percentage
    
    
