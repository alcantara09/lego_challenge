from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from src.domain.entities.user import User
from src.ports.repositories.bricks_repository import BricksRepository
from src.api.dependencies import get_analyse_buildability_use_case, get_brick_repository, get_session
from src.domain.use_cases.analyse_buildability import AnalyseBuildability
from src.api.routers.models import set_to_model, user_to_model

router = APIRouter(prefix="/api", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]
UseCaseDep = Annotated[AnalyseBuildability, Depends(get_analyse_buildability_use_case)]

@router.get("/users/")
async def get_all_users(repository: RepoDep, offset: int = 0, limit: int = 100):
    users = repository.get_all_users()
    if not users:
        return {"data": []}
    user_models = [user_to_model(user) for user in users]
    return {"message": "List of users", "data": [ [model.id, model.name] for model in user_models]}

@router.get("/user/by-id/{user_id}")
async def read_user(repository: RepoDep,user_id: int):
    user = repository.get_user_by_id(user_id)
    if user is None:
        return {"data": []}, status.HTTP_404_NOT_FOUND
    return user_to_model(repository.get_user_by_id(user_id))

@router.get("/user/by-id/{user_id}/possible-sets")
async def read_user_possible_sets(analyse_buildability_use_case: UseCaseDep, user_id: int):
    sets = analyse_buildability_use_case.get_possible_sets_for_user_inventory(user_id)
    if not sets:
        return {"data": []}
    return {"data": [set_to_model(s) for s in sets]}

@router.get("/user/by-id/{user_id}/set/{set_id}/suggest-users")
async def read_user_suggest_users_for_set(analyse_buildability_use_case: UseCaseDep, user_id: int, set_id: int):
    user = analyse_buildability_use_case.bricks_repository.get_user_by_id(user_id)
    suggested_users = analyse_buildability_use_case.suggest_users_for_part_sharing(user, set_id)
    return {"data": suggested_users}

@router.get("/user/by-name/{name}")
async def get_user_by_name(repository: RepoDep, name: str):
    user = repository.get_user_by_name(name)
    if user is None:
        return {"data": []}, status.HTTP_404_NOT_FOUND
    model = user_to_model(user)
    parts = {item.part.name: item.quantity for item in model.inventory.parts}
    return {"data": [[model.id, model.name, parts]]}

@router.get("/users/part-usage/{percentage}")
async def get_parts_with_percentage_of_usage(analyse_buildability_use_case: UseCaseDep, percentage: float = 0.5):
    parts_usage = analyse_buildability_use_case.get_parts_with_percentage_of_usage(percentage)
    return {"data": parts_usage}