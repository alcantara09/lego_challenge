import requests
import uuid
from src.domain.entities.inventory import Inventory, InventoryItem
from src.domain.entities.part import Part
from src.domain.entities.user import User

class UserHarverster:
    BASE_URL = "https://d30r5p5favh3z8.cloudfront.net/api/"

    def __init__(self):
        pass

    def harverst_user_by_id(self, user_id: uuid.UUID) -> User:
        response = requests.get(f"{self.BASE_URL}user/by-id/{user_id}")
        response.raise_for_status()
        user_data = response.json()
        collection = user_data.get("collection", [])
        intentory_items = []
        for item in collection:
            for colour in item.get("variants", []):
                part = Part(
                    id=item.get("pieceId"),
                    material_id=colour.get("color")
                )
                intentory_items.append(InventoryItem(part, colour.get("count")))

        user_entity = User(
            name=user_data.get("username"),
            brick_count=user_data.get("brickCount"),
            inventory=Inventory(parts=intentory_items),
            id=user_data.get("id")
        )

        print(f"Harversted user '{user_data.get("username")}'")
        return user_entity        

    def harverst_all_users(self) -> list[User]:
        response = requests.get(f"{self.BASE_URL}users")
        response.raise_for_status()
        users_data = response.json().get("Users", [])

        user_entities = []

        for user_data in users_data:
            user_entity = self.harverst_user_by_id(uuid.UUID(user_data.get("id")))
            user_entities.append(user_entity)
        return user_entities
    

if __name__ == "__main__":
    harverster = UserHarverster()
    user_entity = harverster.harverst_user_by_id(uuid.UUID("353555ef-3135-4d3a-8e39-c680e1eb26d2"))
    all_users = harverster.harverst_all_users()