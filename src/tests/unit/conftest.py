import pytest

from src.domain.entities.user import User
from src.domain.entities.colour import Colour
from src.domain.entities.shape import Shape
from src.domain.entities.part import Part 
from src.domain.entities.set import Set  
from src.domain.entities.inventory import Inventory

from src.ports.repositories.in_memory_bricks_repository import InMemoryBricksRepository
from src.ports.repositories.bricks_repository import BricksRepository


@pytest.fixture
def basic_parts() -> list[Part]:
    shape_small = Shape(name="Small Brick", id=1)
    shape_big = Shape(name="Big Brick", id=2)

    colour_red = Colour(name="Red", id=1)
    colour_blue = Colour(name="Blue", id=2)
    colour_yellow = Colour(name="Yellow", id=3)

    red_brick_small = Part(name="Red Brick Small", shape=shape_small, colour=colour_red, id=1)
    blue_brick_small = Part(name="Blue Brick Small", shape=shape_small, colour=colour_blue, id=2)
    yellow_brick_small = Part(name="Yellow Brick Small", shape=shape_small, colour=colour_yellow, id=3)

    red_brick_big = Part(name="Red Brick Big", shape=shape_big, colour=colour_red, id=4)
    blue_brick_big = Part(name="Blue Brick Big", shape=shape_big, colour=colour_blue, id=5)
    yellow_brick_big = Part(name="Yellow Brick Big", shape=shape_big, colour=colour_yellow, id=6)

    return [
        red_brick_small,
        blue_brick_small,
        yellow_brick_small,
        red_brick_big,
        blue_brick_big,
        yellow_brick_big
    ]

@pytest.fixture
def basic_sets(basic_parts: list[Part]) -> list[Set]:
    set1 = Set(name="Small Set", required_parts={
        basic_parts[0].id: 4,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1
    }, 
    id=1)

    set2 = Set(name="Big Set", required_parts={
        basic_parts[0].id: 5,
        basic_parts[1].id: 3,
        basic_parts[2].id: 2,
        basic_parts[3].id: 6,
        basic_parts[4].id: 4,
    },
    id=2)

    return [set1, set2]

@pytest.fixture
def basic_users(basic_parts: list[Part]) -> list[User]:
    inventory_user_1 = Inventory(parts={
        basic_parts[0].id: 4,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1
    },
    id=1)

    user_1 = User(name="User 1", inventory=inventory_user_1, id=1)

    inventory_user_2 = Inventory(parts={
        basic_parts[0].id: 4,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1
    },
    id=2)

    user_2 = User(name="User 2", inventory=inventory_user_2, id=2)

    inventory_user_3 = Inventory(parts={
        basic_parts[3].id: 6,
        basic_parts[4].id: 4,
    },
    id=3)

    user_3 = User(name="User 3", inventory=inventory_user_3, id=3)

    inventory_user_4 = Inventory(parts={
        basic_parts[5].id: 10
    })

    user_4 = User(name="User 4", inventory=inventory_user_4, id=4)

    return [user_1, user_2, user_3, user_4]

@pytest.fixture
def bricks_repository(basic_parts, basic_sets, basic_users) -> BricksRepository:
    
    in_memory_repo = InMemoryBricksRepository()
    in_memory_repo.sets = [basic_sets[0], basic_sets[1]]
    in_memory_repo.users = [basic_users[0], basic_users[1], basic_users[2], basic_users[3]]
    
    return in_memory_repo

