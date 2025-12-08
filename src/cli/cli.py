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
def get_users():
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
        
        # User info table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "User Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")
        table.add_column("Inventory ID")
        table.add_row(
            str(user["id"]), 
            user["name"],
            str(user["inventory"]["id"])
        )
        console.print(table)

        # Inventory table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Inventory"
        table.add_column("Part ID", style="dim")
        table.add_column("Part Name")
        table.add_column("Colour")
        table.add_column("Shape")
        table.add_column("Quantity", justify="right")
        
        for item in user["inventory"]["parts"]:
            part = item["part"]
            table.add_row(
                str(part["id"]),
                part["name"],
                part["colour"]["name"],
                part["shape"]["name"],
                str(item["quantity"])
            )
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
        data = response.json()["data"]
        
        # data format: [[id, name, {part_name: quantity}]]
        user_id, user_name, parts = data[0]
        
        # User info table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "User Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")
        
        table.add_row(str(user_id), user_name)
        console.print(table)
        
        # Parts table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Inventory"
        table.add_column("Part Name")
        table.add_column("Quantity", justify="right")
        
        for part_name, quantity in parts.items():
            table.add_row(part_name, str(quantity))
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
        table.add_column("Colour")
        table.add_column("Shape")
        table.add_column("Number of Parts", justify="right")
        
        # data format: [[{part}, quantity], ...]
        for item in parts_usage:
            part, quantity = item
            table.add_row(
                str(part["id"]),
                part["name"],
                part["colour"]["name"],
                part["shape"]["name"],
                str(quantity)
            )
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
        
        # data format: [[{user}, shared_parts_count], ...]
        table = Table(show_header=True, header_style="bold magenta")
        table.title = f"Suggested Users for User ID {user_id} and Set ID {set_id}"
        table.add_column("User ID", style="dim")
        table.add_column("User Name")
        table.add_column("Inventory ID")
        table.add_column("Shared Parts Count", justify="right")
        
        for item in suggested_users:
            user, shared_parts_count = item
            table.add_row(
                str(user["id"]),
                user["name"],
                str(user["inventory"]["id"]),
                str(shared_parts_count)
            )
        console.print(table)
        
        # Optional: show detailed inventory for each suggested user
        for item in suggested_users:
            user, shared_parts_count = item
            
            table = Table(show_header=True, header_style="bold cyan")
            table.title = f"{user['name']}'s Inventory"
            table.add_column("Part ID", style="dim")
            table.add_column("Part Name")
            table.add_column("Colour")
            table.add_column("Shape")
            table.add_column("Quantity", justify="right")
            
            for part_item in user["inventory"]["parts"]:
                part = part_item["part"]
                table.add_row(
                    str(part["id"]),
                    part["name"],
                    part["colour"]["name"],
                    part["shape"]["name"],
                    str(part_item["quantity"])
                )
            console.print(table)
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching suggested users: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()