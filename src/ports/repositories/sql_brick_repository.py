from requests import session
from sqlmodel import Session, select
from src.ports.repositories.sql_brick_repository_schema import (
    Colour,
    Shape,
    SetPartLink,
    InventoryPartLink,
    Part,
    Set,
    User,
    Inventory,
)

from src.ports.repositories.bricks_repository import BricksRepository
from src.domain.entities.user import User as DomainUser
from src.domain.entities.inventory import Inventory as DomainInventory
from src.domain.entities.part import Part as DomainPart
from src.domain.entities.set import Set as DomainSet
from src.domain.entities.set import SetItem as DomainSetItem
from src.domain.entities.colour import Colour as DomainColour
from src.domain.entities.shape import Shape as DomainShape
from src.domain.entities.inventory import InventoryItem as DomainInventoryItem


class SQLBrickRepository(BricksRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_colour(self, coulour: DomainColour) -> DomainColour:
        with self.session as session:
            db_colour = Colour(name=coulour.name)
            session.add(db_colour)
            session.commit()
            session.refresh(db_colour)
            return DomainColour(id=db_colour.id, name=db_colour.name)

    def get_all_colours(self) -> list[DomainColour]:
        with self.session as session:
            db_colours = session.exec(select(Colour)).all()
            return [
                DomainColour(id=colour.id, name=colour.name) for colour in db_colours
            ]

    def create_part(self, part: DomainPart) -> DomainPart:
        with self.session as session:
            db_part = Part(
                name=part.id,
                colour_id=part.material_id
            )
            session.add(db_part)
            session.commit()
            session.refresh(db_part)
            return DomainPart(
                id=db_part.id,
                material_id=part.material_id)

    def get_all_parts(self, offset: int = 0, limit: int = 100) -> list[DomainPart]:
        with self.session as session:
            db_parts = session.exec(select(Part)).all()

            return [
                DomainPart(
                    id=row.name, material_id=row.colour_id
                )
                for row in db_parts
            ]

    def create_set(self, lego_set: DomainSet) -> DomainSet:
        with self.session as session:
            # Create set
            #print("Creating set:", lego_set.id)
            if lego_set.id is None:
                raise Exception("Set must have an ID to be created.")
            db_set = Set(name=lego_set.name, id=str(lego_set.id), totalPieces=lego_set.totalPieces)
            session.add(db_set)
            session.flush()
            session.refresh(db_set)
            
            # Create SetPartLink entries for each part
            valid_items = []
            for item in lego_set.parts:
                if item.part.id is None:
                    raise Exception("Part must have an ID to be added to a set.")
                # Check if part existss
                statement = select(Part).where(Part.name == item.part.id, Part.colour_id == item.part.material_id)
                db_part = session.exec(statement).first()
                if db_part is None:
                    db_part = self.create_part(item.part)
                
                set_part_link = SetPartLink(
                    set_id=db_set.id,
                    part_id=db_part.id,
                    quantity=item.quantity
                )
                session.add(set_part_link)
                valid_items.append(item)
            
            session.commit()
            
            return DomainSet(
                id=db_set.id,
                name=db_set.name,
                parts=valid_items,
                totalPieces=db_set.totalPieces
            )

    def get_all_sets(self, offset: int = 0, limit: int = 100) -> list[DomainSet]:
        with self.session as session:
            statement = (
                select(
                    Set.id.label("set_id"),
                    Set.name.label("set_name"),
                    Set.totalPieces.label("total_pieces"),
                    Part.id.label("part_id"),
                    Part.name.label("part_name"),
                    Part.colour_id.label("part_colour_id"),
                    SetPartLink.quantity.label("quantity")
                )
                .outerjoin(SetPartLink, Set.id == SetPartLink.set_id)
                .outerjoin(Part, SetPartLink.part_id == Part.id)
            )
            
            results = session.exec(statement).all()
            
            # Group results by set
            sets_dict: dict[int, dict] = {}
            for row in results:
                set_id = row.set_id
                
                if set_id not in sets_dict:
                    sets_dict[set_id] = {
                        "set_id": row.set_id,
                        "set_name": row.set_name,
                        "total_pieces": row.total_pieces,
                        "items": []
                    }
                
                # Skip if no part (empty set)
                if row.part_id is None:
                    continue
                
                part = DomainPart(id=row.part_name, material_id=row.part_colour_id)
                
                set_item = DomainSetItem(part=part, quantity=row.quantity)
                sets_dict[set_id]["items"].append(set_item)
            
            # Convert to domain objects
            domain_sets = []
            for set_data in sets_dict.values():
                domain_set = DomainSet(
                    id=set_data["set_id"],
                    name=set_data["set_name"],
                    parts=set_data["items"],
                    totalPieces=set_data["total_pieces"]
                )
                domain_sets.append(domain_set)
                #print(set_data["total_pieces"])
            
            return domain_sets

    def get_set_by_id(self, set_id: int) -> DomainSet | None:
        with self.session as session:
            statement = (
                select(
                    Set.id.label("set_id"),
                    Set.name.label("set_name"),
                    Part.id.label("part_id"),
                    Part.name.label("part_name"),
                    Colour.id.label("colour_id"),
                    Colour.name.label("colour_name"),
                    Shape.id.label("shape_id"),
                    Shape.name.label("shape_name"),
                    SetPartLink.quantity.label("quantity")
                )
                .outerjoin(SetPartLink, Set.id == SetPartLink.set_id)
                .outerjoin(Part, SetPartLink.part_id == Part.id)
                .outerjoin(Colour, Part.colour_id == Colour.id)
                .outerjoin(Shape, Part.shape_id == Shape.id)
                .where(Set.id == set_id)
            )
            
            results = session.exec(statement).all()
            
            if not results:
                return None
            
            # Build set items
            items = []
            for row in results:
                # Skip if no part (empty set)
                if row.part_id is None:
                    continue
                
                colour = DomainColour(id=row.colour_id, name=row.colour_name)
                shape = DomainShape(id=row.shape_id, name=row.shape_name)
                part = DomainPart(id=row.part_id, name=row.part_name, colour=colour, shape=shape)
                
                set_item = DomainSetItem(part=part, quantity=row.quantity)
                items.append(set_item)
            
            first_row = results[0]
            return DomainSet(
                id=first_row.set_id,
                name=first_row.set_name,
                parts=items
            )

    def get_set_by_name(self, name: str) -> DomainSet | None:
        with self.session as session:
            statement = (
                select(
                    Set.id.label("set_id"),
                    Set.name.label("set_name"),
                    Set.totalPieces.label("total_pieces"),
                    Part.id.label("part_id"),
                    Part.name.label("part_name"),
                    Part.colour_id.label("part_colour_id"),
                    SetPartLink.quantity.label("quantity")
                )
                .outerjoin(SetPartLink, Set.id == SetPartLink.set_id)
                .outerjoin(Part, SetPartLink.part_id == Part.id)
                .where(Set.name == name)
            )
            
            results = session.exec(statement).all()
            
            if not results:
                return None
            
            # Build set items
            items = []
            for row in results:
                # Skip if no part (empty set)
                if row.part_id is None:
                    continue
                part = DomainPart(id=row.part_name, material_id=row.part_colour_id)
                
                set_item = DomainSetItem(part=part, quantity=row.quantity)
                items.append(set_item)
            
            set_data = results[0]
            return DomainSet(
                    id=set_data[0],
                    name=set_data[1],
                    parts=items,
                    totalPieces=set_data[2]
                )

    def get_parts_by_set_id(self, set_id: int) -> list[DomainSetItem]:
        with self.session as session:
            statement = (
                select(
                    Part.id.label("part_id"),
                    Part.name.label("part_name"),
                    Colour.id.label("colour_id"),
                    Colour.name.label("colour_name"),
                    Shape.id.label("shape_id"),
                    Shape.name.label("shape_name"),
                    SetPartLink.quantity.label("quantity")
                )
                .join(SetPartLink, Part.id == SetPartLink.part_id)
                .join(Colour, Part.colour_id == Colour.id)
                .join(Shape, Part.shape_id == Shape.id)
                .where(SetPartLink.set_id == set_id)
            )
            
            results = session.exec(statement).all()
            
            items = []
            for row in results:
                colour = DomainColour(id=row.colour_id, name=row.colour_name)
                shape = DomainShape(id=row.shape_id, name=row.shape_name)
                part = DomainPart(id=row.part_id, name=row.part_name, colour=colour, shape=shape)
                
                set_item = DomainSetItem(part=part, quantity=row.quantity)
                items.append(set_item)
            
            return items

    def create_inventory(self, inventory: DomainInventory) -> DomainInventory:
        with self.session as session:
            db_inventory = Inventory()
            session.add(db_inventory)
            session.flush()
            session.refresh(db_inventory)

            # Create InventoryPartLink entries for each part
            valid_items = []
            for item in inventory.parts:
                # Check if part exists
                db_part = session.get(Part, item.part.id)
                if db_part is None:
                    raise ValueError(f"Part with id {item.part.id} does not exist")

                inventory_part_link = InventoryPartLink(
                    inventory_id=db_inventory.id,
                    part_id=item.part.id,
                    quantity=item.quantity,
                )
                session.add(inventory_part_link)
                valid_items.append(item)

            session.commit()

            # Return DomainInventory with the new structure
            return DomainInventory(id=db_inventory.id, parts=valid_items)

    def get_user_by_id(self, user_id: int) -> DomainUser | None:
        with self.session as session:
            statement = (
                select(
                    User.id.label("user_id"),
                    User.name.label("user_name"),
                    User.brick_count.label("brick_count"),
                    Inventory.id.label("inventory_id"),
                    Part.id.label("part_id"),
                    Part.name.label("part_name"),
                    Part.colour_id.label("part_colour_id"),
                    InventoryPartLink.quantity.label("quantity"),
                )
                .join(Inventory, User.inventory_id == Inventory.id)
                .outerjoin(
                    InventoryPartLink, Inventory.id == InventoryPartLink.inventory_id
                )
                .outerjoin(Part, InventoryPartLink.part_id == Part.id)
                .where(User.id == user_id)
            )

            results = session.exec(statement).all()

            if not results:
                return None

            # Build inventory items
            items = []
            for row in results:
                # Skip if no part (empty inventory)
                if row.part_id is None:
                    continue

                part = DomainPart(
                    id=row.part_name, material_id=row.part_colour_id,
                )

                inventory_item = DomainInventoryItem(part=part, quantity=row.quantity)
                items.append(inventory_item)

            first_row = results[0]
            inventory = DomainInventory(id=first_row.inventory_id, parts=items)

            return DomainUser(
                id=first_row.user_id, name=first_row.user_name, inventory=inventory, brick_count=first_row.brick_count
            )

    def get_user_by_name(self, name: str) -> DomainUser | None:
        with self.session as session:
            statement = (
                select(
                    User.id.label("user_id"),
                    User.name.label("user_name"),
                    User.brick_count.label("brick_count"),
                    Inventory.id.label("inventory_id"),
                    Part.id.label("part_id"),
                    Part.name.label("part_name"),
                    Part.colour_id.label("part_colour_id"),
                    InventoryPartLink.quantity.label("quantity"),
                )
                .join(Inventory, User.inventory_id == Inventory.id)
                .outerjoin(
                    InventoryPartLink, Inventory.id == InventoryPartLink.inventory_id
                )
                .outerjoin(Part, InventoryPartLink.part_id == Part.id)
                .where(User.name == name)
            )

            results = session.exec(statement).all()

            if not results:
                return None

            # Build inventory items
            items = []
            for row in results:
                # Skip if no part (empty inventory)
                if row.part_id is None:
                    continue

                part = DomainPart(
                    id=row.part_name, material_id=row.part_colour_id,
                )

                inventory_item = DomainInventoryItem(part=part, quantity=row.quantity)
                items.append(inventory_item)

            first_row = results[0]
            inventory = DomainInventory(id=first_row.inventory_id, parts=items)

            return DomainUser(
                id=first_row.user_id, name=first_row.user_name, inventory=inventory, brick_count=first_row.brick_count
            )

    def create_user(self, user: DomainUser) -> DomainUser:
        with self.session as session:
            # Create inventory first
            db_inventory = Inventory()
            session.add(db_inventory)
            session.commit()
            session.refresh(db_inventory)

            # Create InventoryPartLink entries for each part
            valid_items = []
            for item in user.inventory.parts:
                # Check if part exists
                statement = select(Part).where(Part.name == item.part.id, Part.colour_id == item.part.material_id)
                db_part = session.exec(statement).first()
                if db_part is None:
                    db_part = self.create_part(item.part)

                inventory_part_link = InventoryPartLink(
                    inventory_id=db_inventory.id,
                    part_id=db_part.id,
                    quantity=item.quantity,
                )
                session.add(inventory_part_link)
                valid_items.append(item)

            session.commit()

            # Create user with inventory
            db_user = User(id=user.id, name=user.name, inventory_id=db_inventory.id, brick_count=user.brick_count)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            #print("Created user with ID:", db_user.id)

            # Return DomainUser with full inventory
            inventory = DomainInventory(id=db_inventory.id, parts=valid_items)

            return DomainUser(id=db_user.id, name=db_user.name, inventory=inventory, brick_count=db_user.brick_count)

    def get_all_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        with self.session as session:
            statement = (
                select(
                    User.id.label("user_id"),
                    User.name.label("user_name"),
                    User.brick_count.label("brick_count"),
                    Inventory.id.label("inventory_id"),
                    Part.id.label("part_id"),
                    Part.name.label("part_name"),
                    Part.colour_id.label("part_colour_id"),
                    InventoryPartLink.quantity.label("quantity"),
                )
                .join(Inventory, User.inventory_id == Inventory.id)
                .outerjoin(
                    InventoryPartLink, Inventory.id == InventoryPartLink.inventory_id
                )
                .outerjoin(Part, InventoryPartLink.part_id == Part.id)
            )

            results = session.exec(statement).all()

            users_dict: dict[int, dict] = {}
            for row in results:
                user_id = row.user_id

                if user_id not in users_dict:
                    users_dict[user_id] = {
                        "user_id": row.user_id,
                        "user_name": row.user_name,
                        "inventory_id": row.inventory_id,
                        "brick_count": row.brick_count,
                        "items": [],
                    }
                part = DomainPart(
                    id=row.part_name, material_id=row.part_colour_id,
                )

                inventory_item = DomainInventoryItem(part=part, quantity=row.quantity)
                users_dict[user_id]["items"].append(inventory_item)

            domain_users = []
            for user_data in users_dict.values():
                inventory = DomainInventory(
                    id=user_data["inventory_id"], parts=user_data["items"]
                )

                user = DomainUser(
                    id=user_data["user_id"],
                    name=user_data["user_name"],
                    inventory=inventory,
                    brick_count=user_data["brick_count"]
                )

                domain_users.append(user)

            return domain_users

