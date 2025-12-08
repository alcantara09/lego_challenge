from src.domain.entities.inventory import Inventory
from src.domain.entities.set import Set
from src.domain.entities.user import User

from src.ports.repositories.bricks_repository import BricksRepository

class AnalyseBuildability:
    def __init__(self, bricks_repository: BricksRepository):
        self.bricks_repository = bricks_repository

    def get_possible_sets_for_user_inventory(self, user_id: int) -> list[Set]:
        user = self.bricks_repository.get_user_by_id(user_id)
        if user is None:
            return []
        inventory = self.bricks_repository.get_inventory_by_id(user.inventory.id)
        if inventory is None:
            return []
        return self.get_possible_sets_from_inventory(inventory)

    def get_possible_sets_from_inventory(self, inventory: Inventory) -> list[Set]:
        all_sets = self.bricks_repository.get_all_sets()
        inventory_parts = {item.part.id: item.quantity for item in inventory.parts}
        
        possible_sets = []
        for target_set in all_sets:
            required_parts = {item.part.id: item.quantity for item in target_set.parts}
            
            if all(inventory_parts.get(part_id, 0) >= qty for part_id, qty in required_parts.items()):
                possible_sets.append(target_set)
        
        return possible_sets
    
    def get_missing_parts_for_set(self, inventory: Inventory, target_set: Set) -> dict[int, int]:
        required_parts = {item.part.id: item.quantity for item in target_set.parts}
        inventory_parts = {item.part.id: item.quantity for item in inventory.parts}
        
        missing_parts = {}
        for part_id, qty in required_parts.items():
            available_qty = inventory_parts.get(part_id, 0)
            if available_qty < qty:
                missing_parts[part_id] = qty - available_qty
        
        return missing_parts
    
    def get_other_users_with_common_parts(self, users: list[User], current_user: User | None, missing_parts: dict[int, int]) -> dict[int, int]:
        users_with_parts = {}
        
        for user in users:
            if current_user is not None and user.id == current_user.id:
                continue
            
            user_part_ids = {item.part.id for item in user.inventory.parts}
            missing_part_ids = set(missing_parts.keys())
            
            number_of_common_parts = len(user_part_ids & missing_part_ids)
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
    
    def suggest_users_for_part_sharing(self, current_user: User, desired_set_id: int) -> dict[int, int]:
        inventory = self.bricks_repository.get_inventory_by_id(current_user.inventory.id)
        if inventory is None:
            return {}
        
        desired_set = self.bricks_repository.get_set_by_id(desired_set_id)
        if desired_set is None:
            return {}
        
        missing_parts = self.get_missing_parts_for_set(inventory, desired_set)
        all_users = self.bricks_repository.get_all_users()
        
        return self.get_other_users_with_common_parts(all_users, current_user, missing_parts)
    
    
    def get_parts_with_percentage_of_usage(self, percentage: float) -> dict[int, int]:
        all_users = self.bricks_repository.get_all_users()
        if not all_users:
            return {}
        
        all_parts = self.bricks_repository.get_all_parts()
        parts_with_usage_above_percentage = {}

        for part in all_parts:
            users_with_part = self.get_other_users_with_part(all_users, part.id)
            if len(users_with_part) / len(all_users) >= percentage:
                number_of_parts = min(users_with_part.values()) if users_with_part else 0
                parts_with_usage_above_percentage[part.id] = number_of_parts
        
        return parts_with_usage_above_percentage
    
    
