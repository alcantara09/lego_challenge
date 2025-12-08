import pytest

from src.domain.entities.user import User
from src.domain.entities.colour import Colour
from src.domain.entities.shape import Shape
from src.domain.entities.part import Part 
from src.domain.entities.set import Set, SetItem
from src.domain.entities.inventory import Inventory, InventoryItem

from src.ports.repositories.in_memory_bricks_repository import InMemoryBricksRepository
from src.ports.repositories.bricks_repository import BricksRepository


@pytest.fixture
def basic_colours() -> list[Colour]:
    return [
        Colour(name="Red", id=1),
        Colour(name="Blue", id=2),
        Colour(name="Yellow", id=3)
    ]


@pytest.fixture
def basic_shapes() -> list[Shape]:
    return [
        Shape(name="Small Brick", id=1),
        Shape(name="Big Brick", id=2)
    ]


@pytest.fixture
def basic_parts(basic_colours: list[Colour], basic_shapes: list[Shape]) -> list[Part]:
    shape_small = basic_shapes[0]
    shape_big = basic_shapes[1]

    colour_red = basic_colours[0]
    colour_blue = basic_colours[1]
    colour_yellow = basic_colours[2]

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
    set1 = Set(
        name="Small Set",
        parts=[
            SetItem(part=basic_parts[0], quantity=4),
            SetItem(part=basic_parts[1], quantity=2),
            SetItem(part=basic_parts[2], quantity=1)
        ],
        id=1
    )

    set2 = Set(
        name="Big Set",
        parts=[
            SetItem(part=basic_parts[0], quantity=5),
            SetItem(part=basic_parts[1], quantity=3),
            SetItem(part=basic_parts[2], quantity=2),
            SetItem(part=basic_parts[3], quantity=6),
            SetItem(part=basic_parts[4], quantity=4)
        ],
        id=2
    )

    return [set1, set2]


@pytest.fixture
def basic_users(basic_parts: list[Part]) -> list[User]:
    inventory_user_1 = Inventory(
        parts=[
            InventoryItem(part=basic_parts[0], quantity=4),
            InventoryItem(part=basic_parts[1], quantity=2),
            InventoryItem(part=basic_parts[2], quantity=1)
        ],
        id=1
    )
    user_1 = User(name="User 1", inventory=inventory_user_1, id=1)

    inventory_user_2 = Inventory(
        parts=[
            InventoryItem(part=basic_parts[0], quantity=4),
            InventoryItem(part=basic_parts[1], quantity=2),
            InventoryItem(part=basic_parts[2], quantity=1)
        ],
        id=2
    )
    user_2 = User(name="User 2", inventory=inventory_user_2, id=2)

    inventory_user_3 = Inventory(
        parts=[
            InventoryItem(part=basic_parts[3], quantity=6),
            InventoryItem(part=basic_parts[4], quantity=4)
        ],
        id=3
    )
    user_3 = User(name="User 3", inventory=inventory_user_3, id=3)

    inventory_user_4 = Inventory(
        parts=[
            InventoryItem(part=basic_parts[5], quantity=10)
        ],
        id=4
    )
    user_4 = User(name="User 4", inventory=inventory_user_4, id=4)

    return [user_1, user_2, user_3, user_4]


@pytest.fixture
def bricks_repository(
    basic_colours: list[Colour],
    basic_shapes: list[Shape],
    basic_parts: list[Part],
    basic_sets: list[Set],
    basic_users: list[User]
) -> BricksRepository:
    in_memory_repo = InMemoryBricksRepository()
    
    # Initialize all collections
    in_memory_repo.colours = basic_colours
    in_memory_repo.shapes = basic_shapes
    in_memory_repo.parts = basic_parts
    in_memory_repo.sets = basic_sets
    in_memory_repo.users = basic_users
    
    # Initialize inventories from users
    in_memory_repo.inventories = [user.inventory for user in basic_users]
    
    # Set next_id to avoid conflicts
    in_memory_repo._next_id = 100
    
    return in_memory_repo

@pytest.fixture
def missing_parts_dict(basic_parts: list[Part]) -> dict[int, int]:
    return {
        basic_parts[0].id: 1,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1,
        basic_parts[3].id: 6,
        basic_parts[4].id: 4
    }