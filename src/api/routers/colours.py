from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.api.dependencies import get_brick_repository, get_session
from src.domain.entities.colour import Colour
from src.ports.repositories.bricks_repository import BricksRepository

router = APIRouter(prefix="/api", tags=["colours"])

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]

@router.get("/colours/")
async def get_all_colours(bricks_repository: RepoDep):
    return bricks_repository.get_all_colours() 