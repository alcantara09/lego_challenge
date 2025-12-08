from pydantic import BaseModel, Field
from src.api.routers.models import UserModel, SetModel, PartModel, ColourModel

class UserSummary(BaseModel):
    """Summary of a user with basic info"""
    id: int = Field(..., description="User unique identifier")
    name: str = Field(..., description="User display name")


class UsersListResponse(BaseModel):
    """Response containing list of users"""
    message: str = Field(default="List of users", description="Response message")
    data: list[UserSummary] = Field(..., description="List of user summaries")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "List of users",
                "data": [
                    {"id": 1, "name": "User 1"},
                    {"id": 2, "name": "User 2"}
                ]
            }
        }


class UserDetailResponse(BaseModel):
    """Detailed user information with inventory"""
    data: UserModel = Field(..., description="User with full inventory details")


class UserByNameData(BaseModel):
    """User data with parts summary"""
    id: int
    name: str
    parts: dict[str, int] = Field(..., description="Part name to quantity mapping")


class UserByNameResponse(BaseModel):
    """Response for user lookup by name"""
    data: list[UserByNameData]

    class Config:
        json_schema_extra = {
            "example": {
                "data": [{
                    "id": 1,
                    "name": "User 1",
                    "parts": {"Red Brick Small": 4, "Blue Brick Small": 2}
                }]
            }
        }


class PossibleSetsResponse(BaseModel):
    """Response containing possible buildable sets"""
    data: list[SetModel] = Field(..., description="List of buildable sets")


class SuggestedUsersItem(BaseModel):
    """A suggested user with shared parts count"""
    user: UserModel
    shared_parts_count: int = Field(..., description="Number of matching parts")


class SuggestedUsersResponse(BaseModel):
    """Response containing suggested users for part sharing"""
    data: list[tuple[UserModel, int]] = Field(..., description="List of [user, shared_count] pairs")


class PartUsageItem(BaseModel):
    """Part with usage statistics"""
    part: PartModel
    min_quantity: int = Field(..., description="Minimum quantity across users")


class PartUsageResponse(BaseModel):
    """Response containing parts usage statistics"""
    data: list[tuple[PartModel, int]] = Field(..., description="List of [part, quantity] pairs")


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str = Field(..., description="Error message")

class SetSummary(BaseModel):
    """Summary of a set with basic info"""
    id: int = Field(..., description="Set unique identifier")
    name: str = Field(..., description="Set display name")


class SetsListResponse(BaseModel):
    """Response containing list of sets"""
    message: str = Field(default="List of sets", description="Response message")
    data: list[SetSummary] = Field(..., description="List of set summaries")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "List of sets",
                "data": [
                    {"id": 1, "name": "Small Set"},
                    {"id": 2, "name": "Big Set"}
                ]
            }
        }


class SetByNameData(BaseModel):
    """Set data with parts summary"""
    id: int = Field(..., description="Set unique identifier")
    name: str = Field(..., description="Set display name")
    parts: dict[str, int] = Field(..., description="Part name to quantity mapping")


class SetByNameResponse(BaseModel):
    """Response for set lookup by name"""
    data: SetByNameData

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "id": 1,
                    "name": "Small Set",
                    "parts": {"Red Brick Small": 4, "Blue Brick Small": 2}
                }
            }
        }


class ColoursListResponse(BaseModel):
    """Response containing list of colours"""
    message: str = Field(default="List of colours", description="Response message")
    data: list[ColourModel] = Field(..., description="List of available colours")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "List of colours",
                "data": [
                    {"id": 1, "name": "Red"},
                    {"id": 2, "name": "Blue"},
                    {"id": 3, "name": "Yellow"}
                ]
            }
        }

class ColourDetailResponse(BaseModel):
    """Response containing single colour details"""
    message: str = Field(default="Colour details", description="Response message")
    data: ColourModel = Field(..., description="Colour information")