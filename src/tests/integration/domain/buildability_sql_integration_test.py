import pytest

from src.domain.entities.part import Part 
from src.domain.entities.set import Set  
from src.domain.entities.inventory import Inventory
from src.ports.repositories.bricks_repository import BricksRepository
from src.domain.use_cases.analyse_buildability import AnalyseBuildability


def test_retrieve_possible_sets_from_inventory(brick_repository_with_data: BricksRepository, analyse_buildability_use_case: AnalyseBuildability):

    # Given
    basic_parts = brick_repository_with_data.get_all_parts()
    #analyse_buildability_use_case = AnalyseBuildability(brick_repository_with_data)


    red_small_brick = next((part for part in basic_parts if part.name == "Red Brick Small"), None)
    blue_small_brick = next((part for part in basic_parts if part.name == "Blue Brick Small"), None)
    yellow_small_brick = next((part for part in basic_parts if part.name == "Yellow Brick Small"), None)

    inventory = Inventory(parts={
        red_small_brick.id: 10,
        blue_small_brick.id: 5,
        yellow_small_brick.id: 2
    })

    # When
    possible_sets = analyse_buildability_use_case.retrieve_possible_sets_from_inventory(inventory)

    # Then
    assert len(possible_sets) == 1
    for set in possible_sets:
        assert set.name == "Small Set"
        assert set.required_parts == {
        red_small_brick.id: 4,
        blue_small_brick.id: 2,
        yellow_small_brick.id: 1
        }

def test_retrieve_possible_sets_from_inventory_not_enough_parts(brick_repository_with_data: BricksRepository, analyse_buildability_use_case: AnalyseBuildability):
    basic_parts = brick_repository_with_data.get_all_parts()

    red_small_brick = next((part for part in basic_parts if part.name == "Red Brick Small"), None)
    blue_small_brick = next((part for part in basic_parts if part.name == "Blue Brick Small"), None)
    yellow_small_brick = next((part for part in basic_parts if part.name == "Yellow Brick Small"), None)

    
    # Given
    inventory = Inventory(parts={
        red_small_brick.id: 4,
        blue_small_brick.id: 1,
        yellow_small_brick.id: 1
    })

    # When
    possible_sets = analyse_buildability_use_case.retrieve_possible_sets_from_inventory(inventory)

    # Then
    assert len(possible_sets) == 0

def test_retrieve_missing_parts_for_set(analyse_buildability_use_case: AnalyseBuildability, brick_repository_with_data: BricksRepository):
    basic_parts = brick_repository_with_data.get_all_parts()
    basic_sets = brick_repository_with_data.get_all_sets()

    red_small_brick = next((part for part in basic_parts if part.name == "Red Brick Small"), None)
    blue_small_brick = next((part for part in basic_parts if part.name == "Blue Brick Small"), None)
    yellow_small_brick = next((part for part in basic_parts if part.name == "Yellow Brick Small"), None)
    red_big_brick = next((part for part in basic_parts if part.name == "Red Brick Big"), None)
    blue_big_brick = next((part for part in basic_parts if part.name == "Blue Brick Big"), None)

    # Given
    inventory = Inventory(parts={
        red_small_brick.id: 4,
        blue_small_brick.id: 1,
        yellow_small_brick.id: 1
    })

    # When
    missing_parts = analyse_buildability_use_case.retrieve_missing_parts_for_set(inventory, basic_sets[1])

    # #Then
    assert missing_parts == {
        red_small_brick.id: 1,
        blue_small_brick.id: 2,
        yellow_small_brick.id: 1,
        red_big_brick.id: 6,
        blue_big_brick.id: 4,
    }
