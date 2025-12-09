
from sqlmodel import SQLModel, create_engine, Session
from src.domain.entities.colour import Colour
from src.domain.entities.set import Set
from src.domain.entities.user import User
from src.ports.repositories.bricks_repository import BricksRepository

from src.client.set_harverster import SetHarverster
from src.client.colour_harverster import ColourHarverster
from src.client.user_harverster import UserHarverster
from src.ports.repositories.sql_brick_repository import SQLBrickRepository

class MigrateDbFromApi:
    def __init__(self, set_harvester: SetHarverster
                 ,colour_harvester: ColourHarverster
                 ,user_harvester: UserHarverster
                 ,bricks_repository: BricksRepository):
        self.set_harvester = set_harvester
        self.colour_harvester = colour_harvester
        self.user_harvester = user_harvester
        self.bricks_repository = bricks_repository
    
    def _migrate_all_colours(self, colours: list[Colour]) -> None:
            for colour in colours:
                self.bricks_repository.create_colour(colour)

    def _migrate_sets(self, sets: list[Set]) -> None:
        for set_data in sets:
            self.bricks_repository.create_set(set_data)

    def _migrate_users(self, users: list[User]):
        for user in users:
            self.bricks_repository.create_user(user)

    def migrate_from_api(self) -> None:
        #colours = self.colour_harvester.harvest_colours()
        #self._migrate_all_colours(colours)

        sets = self.set_harvester.harverst_all_sets()
        self._migrate_sets(sets)

        users = self.user_harvester.harverst_all_users()
        self._migrate_users(users)


def get_session() -> BricksRepository:
    sqlite_url = "sqlite:///:database.db:"
    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield SQLBrickRepository(session)


if __name__ == "__main__":
    set_harverster = SetHarverster()
    colour_harverster = ColourHarverster()
    user_harverster = UserHarverster()

    migrator = MigrateDbFromApi(
        set_harvester=set_harverster,
        colour_harvester=colour_harverster,
        user_harvester=user_harverster,
        bricks_repository=next(get_session())
    )

    migrator.migrate_from_api()

