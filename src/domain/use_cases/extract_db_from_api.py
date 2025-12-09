
from sqlmodel import SQLModel, create_engine, Session
from src.domain.entities.set import Set
from src.domain.entities.user import User
from src.ports.repositories.bricks_repository import BricksRepository

from src.client.set_harverster import SetHarverster
from src.client.user_harverster import UserHarverster
from src.ports.repositories.sql_brick_repository import SQLBrickRepository

class ExtractDbFromApi:
    def __init__(self, set_harvester: SetHarverster
                 ,user_harvester: UserHarverster
                 ,bricks_repository: BricksRepository):
        self.set_harvester = set_harvester
        self.user_harvester = user_harvester
        self.bricks_repository = bricks_repository

    def _migrate_sets(self, sets: list[Set]) -> None:
        for set_data in sets:
            self.bricks_repository.create_set(set_data)

    def _migrate_users(self, users: list[User]):
        for user in users:
            self.bricks_repository.create_user(user)

    def migrate_from_api(self) -> None:
        sets = self.set_harvester.harverst_all_sets()
        self._migrate_sets(sets)

        users = self.user_harvester.harverst_all_users()
        self._migrate_users(users)


