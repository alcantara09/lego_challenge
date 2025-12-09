import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session
from src.domain.entities.user import User
from src.ports.repositories.bricks_repository import BricksRepository
from src.api.dependencies import get_analyse_buildability_use_case, get_brick_repository, get_session
from src.domain.use_cases.analyse_buildability import AnalyseBuildability
from src.api.routers.models import UserModel, set_to_model, user_to_model, part_to_model
from src.api.routers.response_models import ErrorResponse, PartUsageResponse, PossibleSetsResponse, SuggestedUsersResponse, UserByNameData, UserByNameResponse, UserSummary, UsersListResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={
        404: {"model": ErrorResponse, "description": "Resource not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

SessionDep = Annotated[Session, Depends(get_session)]
RepoDep = Annotated[BricksRepository, Depends(get_brick_repository)]
UseCaseDep = Annotated[AnalyseBuildability, Depends(get_analyse_buildability_use_case)]

@router.get(
    "/users/",
    response_model=UsersListResponse,
    status_code=status.HTTP_200_OK,
    summary="Returns a list of users in the catalogue",
    description="Retrieve a paginated list of all users with their basic information.",
    response_description="List of users with ID and name"
)
async def get_all_users(
    repository: RepoDep,
    offset: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return")
):
    users = repository.get_all_users(offset=offset, limit=limit)
    if not users:
        return UsersListResponse(message="List of users", data=[])
    
    user_summaries = [UserSummary(id=user.id, name=user.name) for user in users]
    return UsersListResponse(message="List of users", data=user_summaries)

@router.get(
    "/user/by-id/{user_id}",
    response_model=UserModel,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Retrieve detailed user information including full inventory with parts.",
    responses={
        200: {"description": "User found successfully"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def read_user(
    repository: RepoDep,
    user_id: int = Path(..., gt=0, description="User unique identifier")
):
    logger.info(f"Fetching user with ID: {user_id}")    
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user_to_model(user)

@router.get(
    "/user/by-id/{user_id}/possible-sets",
    response_model=PossibleSetsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get buildable sets for user",
    description="Retrieve all LEGO sets that can be built with the user's current inventory.",
    responses={
        200: {"description": "List of buildable sets"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def read_user_possible_sets(
    analyse_buildability_use_case: UseCaseDep,
    user_id: int = Path(..., gt=0, description="User unique identifier")
):
    logger.info(f"Fetching possible sets for user: {user_id}")
    
    sets = analyse_buildability_use_case.get_possible_sets_for_user_inventory(user_id)
    if not sets:
        return PossibleSetsResponse(data=[])
    return PossibleSetsResponse(data=[set_to_model(s) for s in sets])

@router.get(
    "/user/by-id/{user_id}/set/{set_id}/suggest-users",
    response_model=SuggestedUsersResponse,
    status_code=status.HTTP_200_OK,
    summary="Suggest users for part sharing",
    description="Find other users who have parts that the current user needs to build a specific set.",
    responses={
        200: {"description": "List of suggested users with shared parts count"},
        404: {"model": ErrorResponse, "description": "User or set not found"}
    }
)
async def read_user_suggest_users_for_set(
    analyse_buildability_use_case: UseCaseDep,
    user_id: int = Path(..., gt=0, description="Current user's unique identifier"),
    set_id: int = Path(..., gt=0, description="Target set unique identifier")
):
    logger.info(f"Suggesting users for sharing: user={user_id}, set={set_id}")    

    user = analyse_buildability_use_case.bricks_repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    suggested_users = analyse_buildability_use_case.suggest_users_for_part_sharing(user, set_id)
    
    result = []
    
    for item in suggested_users:
        if isinstance(item, (list, tuple)):
            if len(item) == 2:
                user_or_id, count = item
                if isinstance(user_or_id, int):
                    other_user = analyse_buildability_use_case.bricks_repository.get_user_by_id(user_or_id)
                    if other_user:
                        result.append([user_to_model(other_user), count])
                else:
                    result.append([user_to_model(user_or_id), count])
    
    return SuggestedUsersResponse(data=result)

@router.get(
    "/user/by-name/{name}",
    response_model=UserByNameResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by name",
    description="Retrieve user information by their display name.",
    responses={
        200: {"description": "User found successfully"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def get_user_by_name(
    repository: RepoDep,
    name: str = Path(..., min_length=1, max_length=100, description="User display name")
):
    logger.info(f"Fetching user with name: {name}")

    user = repository.get_user_by_name(name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with name '{name}' not found"
        )
    
    model = user_to_model(user)
    parts = {item.part.name: item.quantity for item in model.inventory.parts}
    
    return UserByNameResponse(
        data=[UserByNameData(id=model.id, name=model.name, parts=parts)]
    )

@router.get(
    "/users/part-usage/",
    response_model=PartUsageResponse,
    status_code=status.HTTP_200_OK,
    summary="Get parts by usage percentage",
    description="Retrieve parts that are owned by at least the specified percentage of users.",
    responses={
        200: {"description": "List of parts with usage above threshold"}
    }
)
async def get_parts_with_percentage_of_usage(
    analyse_buildability_use_case: UseCaseDep,
    brick_repository: RepoDep,
    percentage: float = Query(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Minimum usage percentage (0.0 to 1.0)"
    )
):
    parts_usage = analyse_buildability_use_case.get_parts_with_percentage_of_usage(percentage)
    parts_usage = [[part_to_model(part), quantity] for part, quantity in parts_usage]
    
    return PartUsageResponse(data=parts_usage)