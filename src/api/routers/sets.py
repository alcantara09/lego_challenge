
from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from src.api.routers.response_models import ErrorResponse, SetByNameData, SetByNameResponse, SetSummary, SetsListResponse
from src.ports.repositories.bricks_repository import BricksRepository
from src.api.dependencies import get_brick_repository, get_session
from src.api.routers.models import SetModel, set_to_model

router = APIRouter(
    prefix="/api",
    tags=["sets"],
    responses={
        404: {"model": ErrorResponse, "description": "Resource not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]

@router.get(
    "/sets/",
    response_model=SetsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all sets",
    description="Retrieve a list of all LEGO sets with their basic information.",
    response_description="List of sets with ID and name"
)
async def get_all_sets(bricks_repository: RepoDep):
    sets = bricks_repository.get_all_sets()
    if not sets:
        return SetsListResponse(message="List of sets", data=[])
    
    set_summaries = [SetSummary(id=s.id, name=s.name) for s in sets]
    return SetsListResponse(message="List of sets", data=set_summaries)


@router.get(
    "/set/by-id/{set_id}",
    response_model=SetModel,
    status_code=status.HTTP_200_OK,
    summary="Get set by ID",
    description="Retrieve detailed set information including all required parts.",
    responses={
        200: {"description": "Set found successfully"},
        404: {"model": ErrorResponse, "description": "Set not found"}
    }
)
async def get_set_by_id(
    bricks_repository: RepoDep,
    set_id: int = Path(..., gt=0, description="Set unique identifier")
):
    lego_set = bricks_repository.get_set_by_id(set_id)
    if lego_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with ID {set_id} not found"
        )
    return set_to_model(lego_set)


@router.get(
    "/set/by-name/{name}",
    response_model=SetByNameResponse,
    status_code=status.HTTP_200_OK,
    summary="Get set by name",
    description="Retrieve set information by its display name.",
    responses={
        200: {"description": "Set found successfully"},
        404: {"model": ErrorResponse, "description": "Set not found"}
    }
)
async def get_set_by_name(
    bricks_repository: RepoDep,
    name: str = Path(..., min_length=1, max_length=100, description="Set display name")
):
    lego_set = bricks_repository.get_set_by_name(name)
    if lego_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with name '{name}' not found"
        )
    
    model = set_to_model(lego_set)
    parts = {item.part.name: item.quantity for item in model.parts}
    
    return SetByNameResponse(
        data=SetByNameData(id=model.id, name=model.name, parts=parts)
    )