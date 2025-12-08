from pydantic import BaseModel
from src.domain.entities.user import User
from src.domain.entities.set import Set

# Pydantic Response Models
class ColourModel(BaseModel):
    id: int
    name: str

class ShapeModel(BaseModel):
    id: int
    name: str

class PartModel(BaseModel):
    id: int
    name: str
    colour: ColourModel
    shape: ShapeModel

class InventoryItemModel(BaseModel):
    part: PartModel
    quantity: int

class InventoryModel(BaseModel):
    id: int
    parts: list[InventoryItemModel]

class UserModel(BaseModel):
    id: int
    name: str
    inventory: InventoryModel

class SetItemModel(BaseModel):
    part: PartModel
    quantity: int

class SetModel(BaseModel):
    id: int
    name: str
    parts: list[SetItemModel]

def user_to_model(user: User) -> UserModel:
    inventory_items = [
        InventoryItemModel(
            part=PartModel(
                id=item.part.id,
                name=item.part.name,
                colour=ColourModel(id=item.part.colour.id, name=item.part.colour.name),
                shape=ShapeModel(id=item.part.shape.id, name=item.part.shape.name)
            ),
            quantity=item.quantity
        )
        for item in user.inventory.parts
    ]
    
    return UserModel(
        id=user.id,
        name=user.name,
        inventory=InventoryModel(
            id=user.inventory.id,
            parts=inventory_items
        )
    )

def set_to_model(lego_set: Set) -> SetModel:
    set_items = [
        SetItemModel(
            part=PartModel(
                id=item.part.id,
                name=item.part.name,
                colour=ColourModel(id=item.part.colour.id, name=item.part.colour.name),
                shape=ShapeModel(id=item.part.shape.id, name=item.part.shape.name)
            ),
            quantity=item.quantity
        )
        for item in lego_set.parts
    ]
    
    return SetModel(
        id=lego_set.id,
        name=lego_set.name,
        parts=set_items
    )

def part_to_model(part) -> PartModel:
    return PartModel(
        id=part.id,
        name=part.name,
        colour=ColourModel(id=part.colour.id, name=part.colour.name),
        shape=ShapeModel(id=part.shape.id, name=part.shape.name)
    )

def colour_to_model(colour) -> ColourModel:
    """Convert Colour domain entity to Pydantic ColourModel"""
    return ColourModel(id=colour.id, name=colour.name)