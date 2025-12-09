from sqlmodel import SQLModel, create_engine, Session
import typer
import requests

from rich.console import Console
from rich.table import Table

from src.client.set_harverster import SetHarverster
from src.client.user_harverster import UserHarverster
from src.domain.use_cases.extract_db_from_api import ExtractDbFromApi
from src.ports.repositories.bricks_repository import BricksRepository
from src.ports.repositories.sql_brick_repository import SQLBrickRepository
from src.tests.unit.analyse_buildability_test import AnalyseBuildability

app = typer.Typer(help="CLI tool to visualize buildability analysis from LEGO set.")
console = Console()

def get_repository() -> BricksRepository:
    sqlite_url = "sqlite:///:database.db:"
    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield SQLBrickRepository(session)

@app.command()
def extract_db():
    """
    Extract the database from the API.
    """
    try:
        set_harverster = SetHarverster()
        user_harverster = UserHarverster()

        migrator = ExtractDbFromApi(set_harvester=set_harverster, user_harvester=user_harverster, bricks_repository=next(get_repository()))

        migrator.migrate_from_api()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error initiating database migration: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def get_possible_sets():
    """
    Get all possible Sets for brickfan35.
    """
    try:

        analyse_buildability_use_case = AnalyseBuildability(next(get_repository()))
        bricks_repository = next(get_repository())
        user = bricks_repository.get_user_by_name("brickfan35")
        possible_sets = analyse_buildability_use_case.get_possible_sets_for_user_inventory(user.id)

        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Possible Sets for brickfan35"
        table.add_column("Name")  
        table.add_column("Total Parts", justify="right")      
        for lego_set in possible_sets:
            table.add_row(lego_set.name, str(lego_set.totalPieces))            
        console.print(table)

    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching users: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def suggest_users():
    """
    Suggest users for part sharing to build tropical-island for landscape-artist.
    """
    try:
        analyse_buildability_use_case = AnalyseBuildability(next(get_repository()))
        brick_repository = next(get_repository())
        user = brick_repository.get_user_by_name("landscape-artist")
        users = analyse_buildability_use_case.suggest_users_for_part_sharing(user,"tropical-island")
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Users Suggested for Part Sharing"
        table.add_column("Name")  
        table.add_column("Total Parts", justify="right")     
        for suggested_user, common_parts in users:
            table.add_row(suggested_user.name, str(common_parts))
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching user: {e}[/red]")
        raise typer.Exit(1)
 
@app.command()
def get_part_usage():
    """
    Get parts that more than 50% of users have.
    """
    try: 
        analyse_buildability_use_case = AnalyseBuildability(next(get_repository()))
        parts_most_used = analyse_buildability_use_case.get_parts_with_percentage_of_usage(percentage=0.5)

        table = Table(show_header=True, header_style="bold magenta")
        table.title = f"Parts with Usage Above 50% user ownership"
        table.add_column("Part Name")
        table.add_column("Material ID")
        table.add_column("Min # of parts", justify="right")
        for item in parts_most_used:
            part, quantity = item
            table.add_row(
                str(part.id),
                str(part.material_id),
                str(quantity)
            )
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching part usage: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()