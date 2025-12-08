
from typing import Annotated
from fastapi.params import Depends
from sqlmodel import SQLModel, Session, create_engine
from src.domain.use_cases.analyse_buildability import AnalyseBuildability
from src.ports.repositories.bricks_repository import BricksRepository
from src.ports.repositories.sql_brick_repository import SQLBrickRepository

def get_session() -> Session:
    sqlite_url = "sqlite:///:database.db:"
    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session

def get_brick_repository(session: Annotated[Session, Depends(get_session)]) -> BricksRepository:
    with session as session:
        yield SQLBrickRepository(session)

def get_analyse_buildability_use_case(
    brick_repository: Annotated[BricksRepository, Depends(get_brick_repository)],
) -> AnalyseBuildability:
    yield AnalyseBuildability(brick_repository)