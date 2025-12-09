import pytest

from src.domain.use_cases.analyse_buildability import AnalyseBuildability
from src.ports.repositories.bricks_repository import BricksRepository
from src.ports.repositories.sql_brick_repository import SQLBrickRepository
from sqlmodel import SQLModel, create_engine, Session   

from src.domain.entities.user import User as DomainUser
from src.domain.entities.inventory import Inventory as DomainInventory  


@pytest.fixture
def brick_repository() -> BricksRepository:
    sqlite_url = "sqlite:///:database.db:"
    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield SQLBrickRepository(session)

@pytest.fixture
def analyse_buildability_use_case(brick_repository: BricksRepository) -> AnalyseBuildability:
    return AnalyseBuildability(brick_repository)

def atest_get_user_by_id(brick_repository: BricksRepository):
    user = brick_repository.get_user_by_id("353555ef-3135-4d3a-8e39-c680e1eb26d2")
    print(user)

def atest_get_all_users(brick_repository: BricksRepository):
    users = brick_repository.get_all_users(offset=0, limit=10)
    for user in users:
        print(user)

def atest_get_all_sets(brick_repository: BricksRepository):
    sets = brick_repository.get_all_sets()

def atest_get_set_by_name(brick_repository: BricksRepository):
    lego_set = brick_repository.get_set_by_name("beach-buggy")
    print(lego_set)

def atest_suggest_users_for_part_sharing(analyse_buildability_use_case: AnalyseBuildability, brick_repository: BricksRepository):
    #test for landscape-artist for set tropical-island
    user = brick_repository.get_user_by_id("220053f6-8a3a-45b1-8291-a59845c2b1df")
    users = analyse_buildability_use_case.suggest_users_for_part_sharing(user,"tropical-island")
    print("Suggested users for part sharing with landscape-artist:")
    for suggested_user, common_parts in users:
        print(suggested_user.name, common_parts)


def atest_get_possible_sets_for_user_inventory(analyse_buildability_use_case: AnalyseBuildability):
    #test for brickfan35
    print("Possible sets for user brickfan35:")
    possible_sets = analyse_buildability_use_case.get_possible_sets_for_user_inventory("6d6bc9f2-a762-4a30-8d9a-52cf8d8373fc")
    for lego_set in possible_sets:
        print(lego_set.name)

def test_get_parts_with_percentage_of_usage(analyse_buildability_use_case: AnalyseBuildability, brick_repository: BricksRepository):
    #test for part Red Brick Small
    print("Users with percentage of usage for part Red Brick Small:")
    users_with_percentage = analyse_buildability_use_case.get_parts_with_percentage_of_usage(percentage=0.5)
    for part, percentage in users_with_percentage:
        print(part, percentage)



    
