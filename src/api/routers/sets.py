
from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, status
from src.domain.entities.set import Set
from src.ports.repositories.bricks_repository import BricksRepository
from src.api.dependencies import get_brick_repository, get_session

router = APIRouter(prefix="/api", tags=["sets"])

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]

@router.get("/sets/")
async def get_all_sets(bricks_repository: RepoDep):
    return bricks_repository.get_all_sets()

@router.get("/set/by-id/{set_id}/")
async def get_set_by_id(set_id: int, bricks_repository: RepoDep):
    return bricks_repository.get_set_by_id(set_id) 


@router.get("/set/by-name/{name}")
async def get_set_by_name(name: str, bricks_repository: RepoDep):
    return bricks_repository.get_set_by_name(name)