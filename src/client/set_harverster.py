import requests
import uuid

from src.domain.entities.part import Part
from src.domain.entities.set import Set, SetItem

class SetHarverster:
    BASE_URL = "https://d30r5p5favh3z8.cloudfront.net/api/"

    def __init__(self):
        pass

    def harverst_set_by_name(self, set_name: str) -> dict:
        response = requests.get(f"{self.BASE_URL}set/by-name/{set_name}")
        response.raise_for_status()
        return response.json()
    
    def haverst_set(self, set_id: uuid.UUID) -> dict:
        response = requests.get(f"{self.BASE_URL}set/by-id/{set_id}")
        response.raise_for_status()
        set_data = response.json()

        pieces = set_data.get("pieces", [])

        set_pieces = []
        for part_data, quantity in (
            (piece.get("part", {}), piece.get("quantity", 0)) for piece in pieces
        ):
            part = Part(
                id=part_data.get("designID"),
                material_id=part_data.get("material")
            )
            set_pieces.append(SetItem(part=part, quantity=quantity))

        set_summary = self.harverst_set_by_name(set_data.get("name"))
        total_pieces = set_summary.get("totalPieces")

        print(f"Harversted set '{set_data.get('name')}' with {total_pieces} pieces.")
        set_entity = Set(
            name=set_data.get("name"),
            totalPieces=total_pieces,
            parts=set_pieces,
            id=set_data.get("id")
        )
        if set_entity.id is None:
            raise Exception("Set must have an ID after harvesting.")
        return set_entity
    
    def harverst_all_sets(self) -> list[Set]:
        response = requests.get(f"{self.BASE_URL}sets")
        response.raise_for_status()
        sets_data = response.json()

        set_entities = []

        for set_data in sets_data.get("Sets", []):
            set_entities.append(self.haverst_set(uuid.UUID(set_data.get("id"))) )
        return set_entities
    
