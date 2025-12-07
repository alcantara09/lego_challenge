from sqlmodel import Field, Session, SQLModel, select, Relationship

class Colour(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Shape(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class SetPartLink(SQLModel, table=True):
    set_id: int = Field(foreign_key="set.id", primary_key=True)
    part_id: int = Field(foreign_key="part.id", primary_key=True)
    quantity: int

class InventoryPartLink(SQLModel, table=True):
    inventory_id: int | None = Field(default=None, foreign_key="inventory.id", primary_key=True)
    part_id: int | None = Field(default=None, foreign_key="part.id", primary_key=True)
    quantity: int

class Part(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    shape_id: int = Field(foreign_key="shape.id")
    colour_id: int = Field(foreign_key="colour.id")
    sets: list["Set"] = Relationship(back_populates="parts", link_model=SetPartLink)
    inventories: list["Inventory"] = Relationship(back_populates="parts", link_model=InventoryPartLink)

class Set(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    parts: list[Part] = Relationship(back_populates="sets", link_model=SetPartLink)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    inventory_id: int = Field(foreign_key="inventory.id")

class Inventory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parts: list[Part] = Relationship(back_populates="inventories", link_model=InventoryPartLink)