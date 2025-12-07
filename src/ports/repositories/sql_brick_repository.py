from sqlmodel import Field, Session, SQLModel, select, Relationship


from src.ports.repositories.sql_brick_repository_schema import Colour, Shape, SetPartLink, InventoryPartLink, Part, Set, User, Inventory

from src.ports.repositories.bricks_repository import BricksRepository
from src.domain.entities.user import User as DomainUser
from src.domain.entities.inventory import Inventory as DomainInventory
from src.domain.entities.part import Part as DomainPart
from src.domain.entities.set import Set as DomainSet
from src.domain.entities.colour import Colour as DomainColour
from src.domain.entities.shape import Shape as DomainShape



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
        
    def get_colour_by_id(self, colour_id: int) -> DomainColour:
        with self.session as session:
            db_colour = session.get(Colour, colour_id)
            return DomainColour(id=db_colour.id, name=db_colour.name)

    def get_all_colours(self) -> list[DomainColour]:
        with self.session as session:
            db_colours = session.exec(select(Colour)).all()
            return [DomainColour(id=colour.id, name=colour.name) for colour in db_colours]
        
    def create_shape(self, shape: DomainShape) -> DomainShape:
        with self.session as session:
            db_shape = Shape(name=shape.name)
            session.add(db_shape)
            session.commit()
            session.refresh(db_shape)
            return DomainShape(id=db_shape.id, name=db_shape.name)
    
    def get_shape_by_id(self, shape_id: int) -> DomainShape:
        with self.session as session:
            db_shape = session.get(Shape, shape_id)
            return DomainShape(id=db_shape.id, name=db_shape.name)
        
    def create_part(self, part: DomainPart) -> DomainPart:
        with self.session as session:
            db_part = Part(name=part.name, colour_id=part.colour.id, shape_id=part.shape.id)
            session.add(db_part)
            session.commit()
            session.refresh(db_part)
            colour = DomainColour(id=part.colour.id, name=part.colour.name)
            shape = DomainShape(id=part.shape.id, name=part.shape.name)
            return DomainPart(id=db_part.id, name=db_part.name, colour=colour, shape=shape)

    def get_part_by_id(self, part_id: int) -> DomainPart | None:
        with self.session as session:
            db_part = session.get(Part, part_id)
            if not db_part:
                return None
            
            colour = self.get_colour_by_id(db_part.colour_id)
            shape = self.get_shape_by_id(db_part.shape_id)
            return DomainPart(id=db_part.id, name=db_part.name, colour=colour,  shape=shape)


    def get_all_parts(self) -> list[DomainPart]:
        with self.session as session:
            parts = session.exec(select(Part)).all()
            return [DomainPart(id=part.id, name=part.name,
                               colour=DomainColour(id=part.colour.id, name=part.colour.name),
                               shape=DomainShape(id=part.shape.id, name=part.shape.name)) for part in parts]
        
    def get_part_quantity_in_set(self, set_id: int, part_id: int) -> int:
        with self.session as session:
            statement = select(SetPartLink).where(
                SetPartLink.set_id == set_id,
                SetPartLink.part_id == part_id
            )
            link = session.exec(statement).first()
            if link:
                return link.quantity
            return 0
    
    def get_part_quantity_in_inventory(self, inventory_id: int, part_id: int) -> int:
        with self.session as session:
            statement = select(InventoryPartLink).where(
                InventoryPartLink.inventory_id == inventory_id,
                InventoryPartLink.part_id == part_id
            )
            link = session.exec(statement).first()
            if link:
                return link.quantity
            return 0

    def create_set(self, set: DomainSet) -> DomainSet:
        with self.session as session:    
            db_set = Set(name=set.name)
            session.add(db_set)
            session.flush()

            for part_id, qty in set.required_parts.items():
                db_part = session.get(Part, part_id)
                if not db_part:
                    raise ValueError(f"Part with id {part_id} does not exist.")
                    
                else:
                    link = SetPartLink(set_id=db_set.id, part_id=part_id, quantity=qty)
                    session.add(link)
            
            session.commit()
            session.refresh(db_set)

            parts = {}
            for link in db_set.parts:
                quantity = self.get_part_quantity_in_set(db_set.id, link.id)
                parts[link.id] = quantity

            set = DomainSet(id=db_set.id, name=db_set.name, required_parts=parts)
            return db_set

    def get_all_sets(self) -> list[DomainSet]:
        with self.session as session:
            sets = []
            db_sets = session.exec(select(Set)).all()
            for db_set in db_sets:
                parts = {}
                for link in db_set.parts:
                    quantity = self.get_part_quantity_in_set(db_set.id, link.id)
                    parts[link.id] = quantity
                set_entity = DomainSet(id=db_set.id, name=db_set.name, required_parts=parts)
                sets.append(set_entity)
            return sets
        
    def get_parts_by_set_id(self, set_id: int) -> dict[int, int]:
        with self.session as session:
            set_obj = session.get(Set, set_id)
            if not set_obj:
                return {}
            parts_dict = {}
            for link in set_obj.parts:
                quantity = self.get_part_quantity_in_set(set_obj.id, link.id)
                parts_dict[link.id] = quantity
            return parts_dict

    def create_inventory(self, inventory: DomainInventory) -> DomainInventory:
        with self.session as session:    
            db_inventory = Inventory()
            session.add(db_inventory)
            session.flush()

            for part_id, qty in inventory.parts.items():
                db_part = session.get(Part, part_id)
                if not db_part:
                    raise ValueError(f"Part with id {part_id} does not exist.")
                    
                else:
                    link = InventoryPartLink(inventory_id=db_inventory.id, part_id=part_id, quantity=qty)
                    session.add(link)
            
            session.commit()
            session.refresh(db_inventory)
            parts = {}
            for link in db_inventory.parts:
                quantity = self.get_part_quantity_in_inventory(db_inventory.id, link.id)
                parts[link.id] = quantity

            inventory = DomainInventory(id=db_inventory.id, parts=parts)
            return inventory
        
    def get_inventory_by_id(self, inventory_id: int) -> DomainInventory:
        with self.session as session:
            db_inventory = session.get(Inventory, inventory_id)
            if not db_inventory:
                return None
            parts = {}
            for link in db_inventory.parts:
                quantity = self.get_part_quantity_in_inventory(db_inventory.id, link.id)
                parts[link.id] = quantity
            inventory = DomainInventory(id=db_inventory.id, parts=parts)
            return inventory
    
    def get_parts_by_inventory_id(self, inventory_id: int) -> dict[int, int]:
        with self.session as session:
            inventory_obj = session.get(Inventory, inventory_id)
            if not inventory_obj:
                return {}
            parts_dict = {}
            for link in inventory_obj.parts:
                quantity = self.get_part_quantity_in_inventory(inventory_obj.id, link.id)
                parts_dict[link.id] = quantity
            return parts_dict

    def get_user_by_id(self, user_id: int) -> DomainUser:
        with self.session as session:
            db_user = session.get(User, user_id)
            if not db_user:
                return None
            print
            inventory = self.get_inventory_by_id(db_user.inventory_id)
            print("Fetched Inventory for User:", inventory)
            return DomainUser(id=db_user.id, name=db_user.name, inventory=inventory)

    def create_user(self, user: DomainUser) -> DomainUser:
        with self.session as session:           
            entity_inventory = self.create_inventory(user.inventory)
            user = User(name=user.name, inventory_id=entity_inventory.id)
            session.add(user)
            session.commit()
            session.refresh(user)

            return self.get_user_by_id(user.id)    

    def get_all_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        with self.session as session:
            users = []
            db_users = session.exec(select(User).offset(offset).limit(limit)).all()
            for db_user in db_users:
                inventory = self.get_inventory_by_id(db_user.inventory_id)
                user = DomainUser(id=db_user.id, name=db_user.name, inventory=inventory)
                users.append(user)
            return users
        
    def get_inventory_of_user(self, user_id: int) -> DomainInventory:
        with self.session as session:
            user = session.get(User, user_id)
            if not user:
                return None
            inventory = session.get(Inventory, user.inventory_id)
            return inventory
