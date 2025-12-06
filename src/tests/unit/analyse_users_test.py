import pytest

from src.ports.repositories.bricks_repository import BricksRepository
from src.domain.use_cases.analyse_users import AnalyseUsers
from src.domain.entities.part import Part
from src.domain.entities.inventory import Inventory
from src.domain.entities.user import User

@pytest.fixture
def analyse_users_use_case(bricks_repository: BricksRepository) -> AnalyseUsers:
    return AnalyseUsers(bricks_repository)

@pytest.fixture
def missing_parts(basic_parts) -> Inventory:
    return Inventory(parts={
        basic_parts[0].id: 1,
        basic_parts[1].id: 2,
        basic_parts[2].id: 1,
        basic_parts[3].id: 6,
        basic_parts[4].id: 4
    })

def test_retrieve_other_users_with_parts(analyse_users_use_case: AnalyseUsers, basic_parts: list[Part], missing_parts: Inventory, basic_users: list[User]):
    # When
    users_with_parts = analyse_users_use_case.retrieve_other_users_with_parts(basic_users[0], missing_parts)
    
    # Then
    assert len(users_with_parts) == 2
    users_ids = list(users_with_parts.keys())
    
    assert users_ids[0] == basic_users[1].id
    assert users_ids[1] == basic_users[2].id
    
