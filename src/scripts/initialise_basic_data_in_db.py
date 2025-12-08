from sqlmodel import SQLModel, Session, create_engine

from src.domain.entities.colour import Colour
from src.domain.entities.shape import Shape
from src.domain.entities.part import Part
from src.domain.entities.set import Set
from src.domain.entities.inventory import Inventory
from src.domain.entities.user import User

from src.ports.repositories.sql_brick_repository import SQLBrickRepository

sqlite_url = "sqlite:///:database.db:"
engine = create_engine(sqlite_url, echo=False)
SQLModel.metadata.create_all(engine)


with Session(engine) as session:
    brick_repository = SQLBrickRepository(session)
    # Initialise basic data

    red_colour = Colour(name="Red")
    blue_colour = Colour(name="Blue")
    yellow_colour = Colour(name="Yellow")

    red_colour = brick_repository.create_colour(red_colour)
    blue_colour = brick_repository.create_colour(blue_colour)
    yellow_colour = brick_repository.create_colour(yellow_colour)

    shape_small = Shape(name="Small Brick")
    shape_big = Shape(name="Big Brick")
    shape_small = brick_repository.create_shape(shape_small)
    shape_big = brick_repository.create_shape(shape_big)

    red_brick_small = Part(name="Red Brick Small", colour=red_colour, shape=shape_small)
    blue_brick_small = Part(name="Blue Brick Small", colour=blue_colour, shape=shape_small)
    yellow_brick_small = Part(name="Yellow Brick Small", colour=yellow_colour, shape=shape_small)
    red_brick_small = brick_repository.create_part(red_brick_small)
    blue_brick_small = brick_repository.create_part(blue_brick_small)
    yellow_brick_small = brick_repository.create_part(yellow_brick_small)

    red_brick_big = Part(name="Red Brick Big", colour=red_colour, shape=shape_big)
    blue_brick_big = Part(name="Blue Brick Big", colour=blue_colour, shape=shape_big)
    yellow_brick_big = Part(name="Yellow Brick Big", colour=yellow_colour, shape=shape_big)
    red_brick_big = brick_repository.create_part(red_brick_big)
    blue_brick_big = brick_repository.create_part(blue_brick_big)
    yellow_brick_big = brick_repository.create_part(yellow_brick_big)

    set1 = Set(
        name="Small Set",
        required_parts={
            red_brick_small.id: 4,
            blue_brick_small.id: 2,
            yellow_brick_small.id: 1,
        },
    )
    set2 = Set(
        name="Big Set",
        required_parts={
            red_brick_small.id: 5,
            blue_brick_small.id: 3,
            yellow_brick_small.id: 2,
            red_brick_big.id: 6,
            blue_brick_big.id: 4,
        },
    )
    set1 = brick_repository.create_set(set1)
    set2 = brick_repository.create_set(set2)

    inventory_user_1 = Inventory(parts={
        red_brick_small.id: 4,
        blue_brick_small.id: 2,
        yellow_brick_small.id: 1
    })

    user_1 = User(name="User 1", inventory=inventory_user_1)

    inventory_user_2 = Inventory(parts={
        red_brick_small.id: 4,
        blue_brick_small.id: 2,
        yellow_brick_small.id: 1
    })

    user_2 = User(name="User 2", inventory=inventory_user_2)

    inventory_user_3 = Inventory(parts={
        red_brick_big.id: 6,
        blue_brick_big.id: 4,
    })

    user_3 = User(name="User 3", inventory=inventory_user_3)

    inventory_user_4 = Inventory(parts={
        yellow_brick_big.id: 10
    })

    user_4 = User(name="User 4", inventory=inventory_user_4)

    brick_repository.create_user(user_1)
    brick_repository.create_user(user_2)
    brick_repository.create_user(user_3)
    brick_repository.create_user(user_4)