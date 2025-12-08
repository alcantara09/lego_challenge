import typer
import requests
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print_json
import json

app = typer.Typer(help="CLI tool to interact with REST APIs")
console = Console()

url_base = "http://127.0.0.1:8000"

@app.command()
def list_users():
    """
    List all users from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/users/")
        response.raise_for_status()
        users = response.json()["data"]
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "User Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")        
        for user in users:
            table.add_row(str(user[0]), user[1])        
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching users: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def get_user_by_id(id: int):
    """
    Get a user by ID from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/user/by-id/{id}")
        response.raise_for_status()
        user = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "User Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")        
        table.add_row(str(user["id"]), user["name"])        
        console.print(table)

        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Inventory"
        table.add_column("Part ID", style="dim")
        table.add_column("Part Name")
        table.add_column("Quantity", justify="right")
        for part_id, qty in user["inventory"]["parts"].items():
            table.add_row(str(part_id), "part[part_name]", str(qty))
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching user: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def get_user_by_name(name: str):
    """
    Get a user by name from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/user/by-name/{name}")
        response.raise_for_status()
        user = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "User Information"
        table.add_column("ID", style="dim")
        table.add_column("Name") 
        table.add_column("Number of Parts")       
        table.add_row(str(user["id"]), user["name"], str(len(user["inventory"]["parts"])))        
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching user: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def get_sets():
    """
    List all sets from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/sets/")
        response.raise_for_status()
        sets = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Sets Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")        
        for set_ in sets:
             table.add_row(str(set_["id"]), set_["name"])        
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching sets: {e}[/red]")
        raise typer.Exit(1)
    
@app.command()
def get_set_by_name(name: str):
    """
    Get a set by name from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/set/by-name/{name}")
        response.raise_for_status()
        brick_set = response.json()
        print(brick_set)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Set Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")
        table.add_column("Number of Parts")
        table.add_row(str(brick_set["id"]), brick_set["name"], str(len(brick_set["required_parts"])))
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching set: {e}[/red]")
        raise typer.Exit(1)
    
@app.command()
def get_set_by_id(id: int):
    """
    Get a set by ID from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/set/by-id/{id}")
        response.raise_for_status()
        brick_set = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Set Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")
        table.add_column("Number of Parts")
        table.add_row(str(brick_set["id"]), brick_set["name"], str(len(brick_set["required_parts"])))
        console.print(table)

        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Required Parts"
        table.add_column("Part ID", style="dim")
        table.add_column("Part Name")
        table.add_column("Quantity", justify="right")
        for part_id, qty in brick_set["required_parts"].items():
            table.add_row(str(part_id), "part[part_name]", str(qty))
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching set: {e}[/red]")
        raise typer.Exit(1)
    
@app.command()
def get_colours():
    """
    List all colours from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/colours/")
        response.raise_for_status()
        colours = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Colours Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")        
        for colour in colours:
             table.add_row(str(colour["id"]), colour["name"])        
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching colours: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def get_part_usage(percentage: float = 0.5):
    """
    Get parts with usage above a certain percentage from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/users/part-usage/{percentage}")
        response.raise_for_status()
        parts_usage = response.json()["data"]
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = f"Parts with Usage Above {percentage*100}%"
        table.add_column("Part ID", style="dim")
        table.add_column("Part Name")
        table.add_column("Usage Percentage", justify="right")
        for part in parts_usage:
            table.add_row(str(part["part_id"]), part["part_name"], f"{part['usage_percentage']*100:.2f}%")
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching part usage: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def suggest_users(user_id: int, set_id: int):
    """
    Suggest users for part sharing based on a user's missing parts for a set.
    """
    try:
        response = requests.get(f"{url_base}/api/user/by-id/{user_id}/set/{set_id}/suggest-users")
        response.raise_for_status()
        suggested_users = response.json()["data"]
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = f"Suggested Users for User ID {user_id} and Set ID {set_id}"
        table.add_column("User ID", style="dim")
        table.add_column("User Name")
        table.add_column("Shared Parts Count", justify="right")
        for user in suggested_users:
            table.add_row(str(user["user_id"]), user["user_name"], str(user["shared_parts_count"]))
        console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching suggested users: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()