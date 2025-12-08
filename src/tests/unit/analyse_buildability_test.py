import pytest

from src.domain.entities.part import Part 
from src.domain.entities.set import Set, SetItem
from src.domain.entities.user import User
from src.domain.entities.inventory import Inventory, InventoryItem
from src.ports.repositories.bricks_repository import BricksRepository
from src.domain.use_cases.analyse_buildability import AnalyseBuildability

@pytest.fixture
def analyse_buildability_use_case(bricks_repository: BricksRepository) -> AnalyseBuildability:
    return AnalyseBuildability(bricks_repository)

def test_get_possible_sets_from_inventory(analyse_buildability_use_case: AnalyseBuildability, basic_parts: list[Part]):
    # Given
    inventory = Inventory(parts=[
        InventoryItem(part=basic_parts[0], quantity=4),
        InventoryItem(part=basic_parts[1], quantity=2),
        InventoryItem(part=basic_parts[2], quantity=1)
    ])

    # When
    possible_sets = analyse_buildability_use_case.get_possible_sets_from_inventory(inventory)

    # Then
    assert len(possible_sets) == 1
    for lego_set in possible_sets:
        assert lego_set.name == "Small Set"
        
        # Verify parts using list[SetItem]
        parts_dict = {item.part.id: item.quantity for item in lego_set.parts}
        assert parts_dict[basic_parts[0].id] == 4
        assert parts_dict[basic_parts[1].id] == 2
        assert parts_dict[basic_parts[2].id] == 1

def test_get_possible_sets_from_inventory_not_enough_parts(analyse_buildability_use_case: AnalyseBuildability, basic_parts: list[Part]):
    # Given
    inventory = Inventory(parts=[
        InventoryItem(part=basic_parts[0], quantity=4),
        InventoryItem(part=basic_parts[1], quantity=1),
        InventoryItem(part=basic_parts[2], quantity=1)
    ])

    # When
    possible_sets = analyse_buildability_use_case.get_possible_sets_from_inventory(inventory)

    # Then
    assert len(possible_sets) == 0

def test_get_missing_parts_for_set(analyse_buildability_use_case: AnalyseBuildability, basic_parts: list[Part], basic_sets: list[Set]):
    # Given
    inventory = Inventory(parts=[
        InventoryItem(part=basic_parts[0], quantity=4),
        InventoryItem(part=basic_parts[1], quantity=1),
        InventoryItem(part=basic_parts[2], quantity=1)
    ])
    # When
    missing_parts = analyse_buildability_use_case.get_missing_parts_for_set(inventory, basic_sets[1])
    # Then
    assert missing_parts == {
        basic_parts[0].id: 1,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1,
        basic_parts[3].id: 6,
        basic_parts[4].id: 4,
    }

def test_get_other_users_with_parts(
    analyse_buildability_use_case: AnalyseBuildability, 
    basic_parts: list[Part], 
    missing_parts_dict: dict[int, int], 
    basic_users: list[User]
):
    # When
    users_with_parts = analyse_buildability_use_case.get_other_users_with_common_parts(
        basic_users, 
        basic_users[0], 
        missing_parts_dict
    )
    
    # Then
    assert len(users_with_parts) == 2
    users_ids = list(users_with_parts.keys())
    
    assert users_ids[0] == basic_users[1].id
    assert users_ids[1] == basic_users[2].id

def test_get_possible_sets_for_user_inventory_user_not_found(
    analyse_buildability_use_case: AnalyseBuildability
):
    # When
    possible_sets = analyse_buildability_use_case.get_possible_sets_for_user_inventory(9999)

    # Then
    assert possible_sets == []

def test_get_missing_parts_for_set_empty_inventory(
    analyse_buildability_use_case: AnalyseBuildability,
    basic_sets: list[Set]
):
    # Given
    inventory = Inventory(parts=[])

    # When
    missing_parts = analyse_buildability_use_case.get_missing_parts_for_set(inventory, basic_sets[0])

    # Then
    parts_dict = {item.part.id: item.quantity for item in basic_sets[0].parts}
    assert missing_parts == parts_dict

def test_get_possible_sets_from_inventory_empty_inventory(
    analyse_buildability_use_case: AnalyseBuildability
):
    # Given
    inventory = Inventory(parts=[])

    # When
    possible_sets = analyse_buildability_use_case.get_possible_sets_from_inventory(inventory)

    # Then
    assert len(possible_sets) == 0