from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.api.dependencies import get_brick_repository, get_session
from src.api.routers.response_models import ErrorResponse
from src.ports.repositories.bricks_repository import BricksRepository
from src.api.routers.response_models import ColoursListResponse
from src.api.routers.models import colour_to_model
from fastapi import status

router = APIRouter(
    prefix="/api",
    tags=["colours"],
    responses={
        404: {"model": ErrorResponse, "description": "Resource not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]

@router.get(
    "/colours/",
    response_model=ColoursListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all colours",
    description="Retrieve a list of all available LEGO brick colours.",
    response_description="List of colours with ID and name"
)
async def get_all_colours(bricks_repository: RepoDep):
    colours = bricks_repository.get_all_colours()
    if not colours:
        return ColoursListResponse(message="List of colours", data=[])
    
    colour_models = [colour_to_model(c) for c in colours]
    return ColoursListResponse(message="List of colours", data=colour_models)
