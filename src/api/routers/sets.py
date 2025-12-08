
from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, status
from src.domain.entities.set import Set
from src.ports.repositories.bricks_repository import BricksRepository
from src.api.dependencies import get_brick_repository, get_session
from src.api.routers.models import set_to_model

router = APIRouter(prefix="/api", tags=["sets"])

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]

@router.get("/sets/")
async def get_all_sets(bricks_repository: RepoDep):
    sets = bricks_repository.get_all_sets()
    if not sets:
        return []
    model_sets = [set_to_model(s) for s in sets]
    return {"data": [[model.id, model.name] for model in model_sets]}

@router.get("/set/by-id/{set_id}/")
async def get_set_by_id(set_id: int, bricks_repository: RepoDep):
    lego_set = bricks_repository.get_set_by_id(set_id)
    if lego_set is None:
        return {"data": []} ,status.HTTP_404_NOT_FOUND
    model = set_to_model(lego_set)
    return model

@router.get("/set/by-name/{name}")
async def get_set_by_name(name: str, bricks_repository: RepoDep):
    lego_set = bricks_repository.get_set_by_name(name)
    if lego_set is None:
        return {"data": []}, status.HTTP_404_NOT_FOUND
    model = set_to_model(lego_set)
    parts = {item.part.name: item.quantity for item in model.parts}
    return {"data": [model.id, model.name, parts]}