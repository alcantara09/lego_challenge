from src.domain.entities.inventory import Inventory
from src.domain.entities.set import Set

from src.ports.repositories.bricks_repository import BricksRepository

class AnalyseBuildability:
    def __init__(self, bricks_repository: BricksRepository):
        self.bricks_repository = bricks_repository

    def retrieve_possible_sets_from_inventory(self, inventory: Inventory) -> list[Set]:
        all_sets = self.bricks_repository.get_all_sets()
        possible_sets = []
        for target_set in all_sets:
            required_parts = self.bricks_repository.get_parts_by_set_id(target_set.id)
            if all(inventory.parts.get(part, 0) >= qty for part, qty in required_parts.items()):
                possible_sets.append(target_set)
        return possible_sets
    
    def retrieve_missing_parts_for_set(self, inventory: Inventory, target_set: Set) -> dict:
        required_parts = self.bricks_repository.get_parts_by_set_id(target_set.id)
        missing_parts = {}
        for part_id, qty in required_parts.items():
            available_qty = inventory.parts.get(part_id, 0)
            if available_qty < qty:
                missing_parts[part_id] = qty - available_qty
        return missing_parts
    
    
