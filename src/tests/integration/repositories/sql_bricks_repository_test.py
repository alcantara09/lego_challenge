import pytest

from src.domain.entities.user import User as DomainUser
from src.domain.entities.inventory import Inventory as DomainInventory
from src.domain.entities.inventory import InventoryItem as DomainInventoryItem
from src.domain.entities.part import Part as DomainPart
from src.domain.entities.set import Set as DomainSet
from src.domain.entities.set import SetItem as DomainSetItem
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
    # Setup colour and shape for fake part
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    # Create a fake part that doesn't exist in the database
    fake_part = DomainPart(
        id=9999,
        name="Fake Part",
        colour=db_colour,
        shape=db_shape
    )
    
    # Try to create set with non-existent part
    set_entity = DomainSet(name="Sample Set", parts=[
        DomainSetItem(part=fake_part, quantity=1)
    ])

    with pytest.raises(Exception):
        brick_repository.create_set(set_entity)

def test_create_sample_set_with_part_id(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)

    set_entity = DomainSet(name="Sample Set", parts=[
        DomainSetItem(part=db_part, quantity=2)
    ])
    db_set = brick_repository.create_set(set_entity)

    assert db_set.id is not None
    assert db_set.name == "Sample Set"
    assert len(db_set.parts) == 1
    
    # Verify part details
    item = db_set.parts[0]
    assert item.part.id == db_part.id
    assert item.part.name == "Red 2x4 Brick"
    assert item.part.colour.name == "Red"
    assert item.part.shape.name == "2x4 Brick"
    assert item.quantity == 2

def test_create_sample_inventory_no_part_id(brick_repository: BricksRepository):
    # Setup colour and shape for fake part
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    # Create a fake part that doesn't exist in the database
    fake_part = DomainPart(
        id=9999,
        name="Fake Part",
        colour=db_colour,
        shape=db_shape
    )
    
    # Try to create inventory with non-existent part
    inventory_entity = DomainInventory(parts=[
        DomainInventoryItem(part=fake_part, quantity=5)
    ])
    
    with pytest.raises(ValueError, match="Part with id 9999 does not exist"):
        brick_repository.create_inventory(inventory_entity)

def test_create_sample_inventory_with_part_id(brick_repository: BricksRepository):
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)

    inventory_entity = DomainInventory(parts=[
        DomainInventoryItem(part=db_part, quantity=10)
    ])
    db_inventory = brick_repository.create_inventory(inventory_entity)

    assert db_inventory.id is not None
    assert len(db_inventory.parts) == 1
    
    # Verify part details
    item = db_inventory.parts[0]
    assert item.part.id == db_part.id
    assert item.part.name == "Red 2x4 Brick"
    assert item.quantity == 10

def test_create_sample_user(brick_repository: BricksRepository):
    # Setup colour and shape
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    # Setup part
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)
    
    # Create user with inventory - using new InventoryItem structure
    inventory = DomainInventory(parts=[
        DomainInventoryItem(part=db_part, quantity=10)
    ])
    user = DomainUser(name="sample_user", inventory=inventory)
    
    db_user = brick_repository.create_user(user)
    
    # Verify user
    assert db_user.id is not None
    assert db_user.name == "sample_user"
    
    # Verify inventory
    assert db_user.inventory is not None
    assert len(db_user.inventory.parts) == 1
    
    # Verify part
    item = db_user.inventory.parts[0]
    assert item.part.id == db_part.id
    assert item.quantity == 10

def test_get_all_users(brick_repository: BricksRepository):
    # Setup colours
    red_colour = DomainColour(name="Red")
    blue_colour = DomainColour(name="Blue")
    db_red_colour = brick_repository.create_colour(red_colour)
    db_blue_colour = brick_repository.create_colour(blue_colour)
    
    # Setup shapes
    brick_shape = DomainShape(name="2x4 Brick")
    plate_shape = DomainShape(name="1x2 Plate")
    db_brick_shape = brick_repository.create_shape(brick_shape)
    db_plate_shape = brick_repository.create_shape(plate_shape)
    
    # Setup parts
    red_brick = DomainPart(name="Red 2x4 Brick", colour=db_red_colour, shape=db_brick_shape)
    blue_brick = DomainPart(name="Blue 2x4 Brick", colour=db_blue_colour, shape=db_brick_shape)
    red_plate = DomainPart(name="Red 1x2 Plate", colour=db_red_colour, shape=db_plate_shape)
    db_red_brick = brick_repository.create_part(red_brick)
    db_blue_brick = brick_repository.create_part(blue_brick)
    db_red_plate = brick_repository.create_part(red_plate)
    
    # Create user1 with multiple parts
    inventory1 = DomainInventory(parts=[
        DomainInventoryItem(part=db_blue_brick, quantity=10),
        DomainInventoryItem(part=db_red_brick, quantity=5),
        DomainInventoryItem(part=db_red_plate, quantity=3)
    ])
    user1 = DomainUser(name="user1", inventory=inventory1)
    brick_repository.create_user(user1)

    # Create user2 with single part
    inventory2 = DomainInventory(parts=[
        DomainInventoryItem(part=db_blue_brick, quantity=20)
    ])
    user2 = DomainUser(name="user2", inventory=inventory2)
    brick_repository.create_user(user2)

    # Fetch all users
    users = brick_repository.get_all_users()
    
    # Verify user count
    assert len(users) == 2
    
    # Verify user names
    user_names = [user.name for user in users]
    assert "user1" in user_names
    assert "user2" in user_names
    
    # Get users by name for detailed assertions
    user1_result = next(u for u in users if u.name == "user1")
    user2_result = next(u for u in users if u.name == "user2")
    
    # Verify user1 inventory
    assert user1_result.inventory is not None
    assert user1_result.inventory.id is not None
    assert len(user1_result.inventory.parts) == 3
    
    # Verify user1 parts contain correct data
    user1_parts = {item.part.id: item for item in user1_result.inventory.parts}
    
    assert db_red_brick.id in user1_parts
    assert user1_parts[db_red_brick.id].quantity == 5
    assert user1_parts[db_red_brick.id].part.name == "Red 2x4 Brick"
    assert user1_parts[db_red_brick.id].part.colour.name == "Red"
    assert user1_parts[db_red_brick.id].part.shape.name == "2x4 Brick"
    
    assert db_blue_brick.id in user1_parts
    assert user1_parts[db_blue_brick.id].quantity == 10
    assert user1_parts[db_blue_brick.id].part.name == "Blue 2x4 Brick"
    assert user1_parts[db_blue_brick.id].part.colour.name == "Blue"
    assert user1_parts[db_blue_brick.id].part.shape.name == "2x4 Brick"
    
    assert db_red_plate.id in user1_parts
    assert user1_parts[db_red_plate.id].quantity == 3
    assert user1_parts[db_red_plate.id].part.name == "Red 1x2 Plate"
    assert user1_parts[db_red_plate.id].part.colour.name == "Red"
    assert user1_parts[db_red_plate.id].part.shape.name == "1x2 Plate"
    
    # Verify user2 inventory
    assert user2_result.inventory is not None
    assert user2_result.inventory.id is not None
    assert len(user2_result.inventory.parts) == 1
    
    # Verify user2 parts
    user2_parts = {item.part.id: item for item in user2_result.inventory.parts}
    
    assert db_blue_brick.id in user2_parts
    assert user2_parts[db_blue_brick.id].quantity == 20
    assert user2_parts[db_blue_brick.id].part.name == "Blue 2x4 Brick"
    assert user2_parts[db_blue_brick.id].part.colour.name == "Blue"
    assert user2_parts[db_blue_brick.id].part.shape.name == "2x4 Brick"

def test_get_user_by_name(brick_repository: BricksRepository):
    # Setup colour and shape
    colour = DomainColour(name="Red")
    db_colour = brick_repository.create_colour(colour)
    shape = DomainShape(name="2x4 Brick")
    db_shape = brick_repository.create_shape(shape)
    
    # Setup part
    part = DomainPart(name="Red 2x4 Brick", colour=db_colour, shape=db_shape)
    db_part = brick_repository.create_part(part)
    
    # Create user
    inventory = DomainInventory(parts=[
        DomainInventoryItem(part=db_part, quantity=10)
    ])
    user = DomainUser(name="test_user", inventory=inventory)
    brick_repository.create_user(user)
    
    # Fetch user by name
    fetched_user = brick_repository.get_user_by_name("test_user")
    
    # Verify user
    assert fetched_user is not None
    assert fetched_user.name == "test_user"
    assert fetched_user.inventory is not None
    assert len(fetched_user.inventory.parts) == 1
    
    # Verify part details
    item = fetched_user.inventory.parts[0]
    assert item.part.id == db_part.id
    assert item.part.name == "Red 2x4 Brick"
    assert item.part.colour.name == "Red"
    assert item.part.shape.name == "2x4 Brick"
    assert item.quantity == 10

def test_get_user_by_name_not_found(brick_repository: BricksRepository):
    fetched_user = brick_repository.get_user_by_name("non_existent_user")
    assert fetched_user is None

def test_get_all_parts(brick_repository: BricksRepository):
    # Setup colours
    red_colour = DomainColour(name="Red")
    blue_colour = DomainColour(name="Blue")
    db_red_colour = brick_repository.create_colour(red_colour)
    db_blue_colour = brick_repository.create_colour(blue_colour)
    
    # Setup shapes
    brick_shape = DomainShape(name="2x4 Brick")
    plate_shape = DomainShape(name="1x2 Plate")
    db_brick_shape = brick_repository.create_shape(brick_shape)
    db_plate_shape = brick_repository.create_shape(plate_shape)
    
    # Create parts
    brick_repository.create_part(DomainPart(name="Red Brick", colour=db_red_colour, shape=db_brick_shape))
    brick_repository.create_part(DomainPart(name="Blue Plate", colour=db_blue_colour, shape=db_plate_shape))
    brick_repository.create_part(DomainPart(name="Red Plate", colour=db_red_colour, shape=db_plate_shape))
    
    # Fetch all parts
    parts = brick_repository.get_all_parts()
    
    assert len(parts) == 3
    
    # Verify parts with full details
    parts_dict = {p.name: p for p in parts}
    
    assert "Red Brick" in parts_dict
    assert parts_dict["Red Brick"].colour.name == "Red"
    assert parts_dict["Red Brick"].shape.name == "2x4 Brick"
    
    assert "Blue Plate" in parts_dict
    assert parts_dict["Blue Plate"].colour.name == "Blue"
    assert parts_dict["Blue Plate"].shape.name == "1x2 Plate"
    
    assert "Red Plate" in parts_dict
    assert parts_dict["Red Plate"].colour.name == "Red"
    assert parts_dict["Red Plate"].shape.name == "1x2 Plate"


