from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from src.domain.entities.user import User
from src.ports.repositories.bricks_repository import BricksRepository
from src.api.dependencies import get_analyse_buildability_use_case, get_brick_repository, get_session
from src.domain.use_cases.analyse_buildability import AnalyseBuildability

router = APIRouter(prefix="/api", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]
UseCaseDep = Annotated[AnalyseBuildability, Depends(get_analyse_buildability_use_case)]

@router.get("/users/")
async def get_all_users(repository: RepoDep, offset: int = 0, limit: int = 100):
    users = repository.get_all_users()
    return {"message": "List of users", "data": [[user.id, user.name] for user in users]}

@router.get("/user/by-id/{user_id}")
async def read_user(repository: RepoDep,user_id: int):
    return repository.get_user_by_id(user_id)

@router.get("/user/by-id/{user_id}/possible-sets")
async def read_user_possible_sets(analyse_buildability_use_case: UseCaseDep, user_id: int):
    sets = analyse_buildability_use_case.get_possible_sets_for_user_inventory(user_id)
    return {"possible_sets": "Possible sets for user", "data": [[s.id, s.name] for s in sets]}

@router.get("/user/by-id/{user_id}/set/{set_id}/suggest-users")
async def read_user_suggest_users_for_set(analyse_buildability_use_case: UseCaseDep, user_id: int, set_id: int):
    user = analyse_buildability_use_case.bricks_repository.get_user_by_id(user_id)
    suggested_users = analyse_buildability_use_case.suggest_users_for_part_sharing(user, set_id)
    return {"suggested_users": "Suggested users for part sharing", "data": suggested_users}

@router.get("/user/by-name/{name}")
async def get_user_by_name(repository: RepoDep, name: str):
    return repository.get_user_by_name(name)

@router.get("/users/part-usage/{percentage}")
async def get_parts_with_percentage_of_usage(analyse_buildability_use_case: UseCaseDep, percentage: float = 0.5):
    parts_usage = analyse_buildability_use_case.get_parts_with_percentage_of_usage(percentage)
    return {"parts_usage": "Parts with usage above percentage", "data": parts_usage}