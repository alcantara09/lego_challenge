import pytest

from src.domain.entities.user import User as DomainUser
from src.domain.entities.inventory import Inventory as DomainInventory
from src.domain.entities.part import Part as DomainPart
from src.domain.entities.set import Set as DomainSet
from src.domain.entities.colour import Colour as DomainColour
from src.domain.entities.shape import Shape as DomainShape 
from src.ports.repositories.bricks_repository import BricksRepository

def test_create_sample_colour(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    assert db_colour.id is not None
    assert db_colour.name == "Red"


def test_get_all_colours(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    brick_repository.create_colour(colour)
    colour = DomainColour(name="Blue")
    brick_repository.create_colour(colour)
    colour = DomainColour(name="Yellow")
    brick_repository.create_colour(colour)
    
    colours = brick_repository.get_all_colours()
    assert len(colours) == 3
    colour_names = [colour.name for colour in colours]
    assert "Red" in colour_names
    assert "Blue" in colour_names
    assert "Yellow" in colour_names

def test_create_sample_shape(brick_repository: BricksRepository):
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    assert db_shape.id is not None
    assert db_shape.name == "2x4 Brick"

def test_create_sample_part(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)
    assert db_part.id is not None
    assert db_part.name == "Red 2x4 Brick"
    assert db_part.colour.id == db_colour.id
    assert db_part.shape.id == db_shape.id

def test_create_sample_set_no_part_id(brick_repository: BricksRepository):        
    set_entity = DomainSet(name="Sample Set", required_parts={1: 1})
    with pytest.raises(Exception):
        db_set = brick_repository.create_set(set_entity)

    sets = brick_repository.get_all_sets()
    assert len(sets) == 0

def test_create_sample_set_with_part_id(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)

    set_entity = DomainSet(name="Sample Set", required_parts={db_part.id: 2})
    db_set = brick_repository.create_set(set_entity)

    assert db_set.id is not None
    assert db_set.name == "Sample Set"


def test_get_parts_by_set_id(brick_repository: BricksRepository):
    
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)
    
    set_entity = DomainSet(name="Sample Set", required_parts={db_part.id: 2})
    db_set = brick_repository.create_set(set_entity)

    parts = brick_repository.get_parts_by_set_id(db_set.id)
    assert parts[db_part.id] == 2


def test_create_sample_inventory_no_part_id(brick_repository: BricksRepository):
    inventory_entity = DomainInventory(parts={1: 5})
    with pytest.raises(Exception):
        db_inventory = brick_repository.create_inventory(inventory_entity)

def test_create_sample_inventory_with_part_id(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)

    inventory_entity = DomainInventory(parts={db_part.id: 10})
    db_inventory = brick_repository.create_inventory(inventory_entity)

    assert db_inventory.id is not None
    assert db_inventory.parts[db_part.id] == 10

def test_get_parts_by_inventory_id(brick_repository: BricksRepository):
    
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)
    
    inventory_entity = DomainInventory(parts={db_part.id: 10})
    db_inventory = brick_repository.create_inventory(inventory_entity)
    assert db_inventory.id is not None
    assert db_inventory.parts[db_part.id] == 10

    parts = brick_repository.get_parts_by_inventory_id(db_inventory.id)
    assert parts[db_part.id] == 10

def test_create_sample_user(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)
    
    inventory_entity = DomainInventory(parts={db_part.id: 10})
    user = DomainUser(name="test_user", inventory=inventory_entity)
    db_user = brick_repository.create_user(user)

    assert db_user.id is not None
    assert db_user.name == "test_user"
    assert db_user.inventory.parts[db_part.id] == 10









