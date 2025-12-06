import pytest

from src.domain.entities.part import Part 
from src.domain.entities.set import Set  
from src.domain.entities.inventory import Inventory
from src.ports.repositories.bricks_repository import BricksRepository
from src.domain.use_cases.analyse_buildability import AnalyseBuildability


@pytest.fixture
def analyse_buildability_use_case(bricks_repository: BricksRepository) -> AnalyseBuildability:
    return AnalyseBuildability(bricks_repository)

def test_retrieve_possible_sets_from_inventory(analyse_buildability_use_case: AnalyseBuildability, basic_parts: list[Part]):
    # Given
    inventory = Inventory(parts={
        basic_parts[0].id: 4,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1
    })

    # When
    possible_sets = analyse_buildability_use_case.retrieve_possible_sets_from_inventory(inventory)

    # Then
    assert len(possible_sets) == 1
    for set in possible_sets:
        assert set.name == "Small Set"
        assert set.required_parts == {
        basic_parts[0].id: 4,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1
        }

def test_retrieve_possible_sets_from_inventory_not_enough_parts(analyse_buildability_use_case: AnalyseBuildability, basic_parts: list[Part]):
    # Given
    inventory = Inventory(parts={
        basic_parts[0].id: 4,
        basic_parts[1].id: 1,
        basic_parts[2].id: 1
    })

    # When
    possible_sets = analyse_buildability_use_case.retrieve_possible_sets_from_inventory(inventory)

    # Then
    assert len(possible_sets) == 0

def test_retrieve_missing_parts_for_set(analyse_buildability_use_case: AnalyseBuildability, basic_parts: list[Part], basic_sets: list[Set]):
    # Given
    inventory = Inventory(parts={
        basic_parts[0].id: 4,
        basic_parts[1].id: 1,
        basic_parts[2].id: 1
    })

    # When
    missing_parts = analyse_buildability_use_case.retrieve_missing_parts_for_set(inventory, basic_sets[1])

    # #Then
    assert missing_parts == {
        basic_parts[0].id: 1,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1,
        basic_parts[3].id: 6,
        basic_parts[4].id: 4,
    }
