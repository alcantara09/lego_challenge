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
        response_data = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = response_data["message"]
        table.add_column("ID", style="dim")
        table.add_column("Name")        
        for user in response_data["data"]:
            table.add_row(str(user["id"]), user["name"])        
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
        response_data = response.json()
        user = response_data["data"][0]
        
        # User info table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "User Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")
        table.add_row(str(user["id"]), user["name"])
        console.print(table)
        
        # Parts table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Inventory"
        table.add_column("Part Name")
        table.add_column("Quantity", justify="right")
        
        for part_name, quantity in user["parts"].items():
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
        response_data = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = response_data["message"]
        table.add_column("ID", style="dim")
        table.add_column("Name")        
        for set_ in response_data["data"]:
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
        response_data = response.json()
        brick_set = response_data["data"]
        
        # Set info table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Set Information"
        table.add_column("ID", style="dim")
        table.add_column("Name")
        table.add_column("Number of Parts")
        table.add_row(
            str(brick_set["id"]), 
            brick_set["name"], 
            str(len(brick_set["parts"]))
        )
        console.print(table)
        
        # Parts table
        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Required Parts"
        table.add_column("Part Name")
        table.add_column("Quantity", justify="right")
        
        for part_name, quantity in brick_set["parts"].items():
            table.add_row(part_name, str(quantity))
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
        table.add_row(
            str(brick_set["id"]), 
            brick_set["name"], 
            str(len(brick_set["parts"]))
        )
        console.print(table)

        table = Table(show_header=True, header_style="bold magenta")
        table.title = "Required Parts"
        table.add_column("Part ID", style="dim")
        table.add_column("Part Name")
        table.add_column("Colour")
        table.add_column("Shape")
        table.add_column("Quantity", justify="right")
        
        for item in brick_set["parts"]:
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
        response_data = response.json()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.title = response_data["message"]
        table.add_column("ID", style="dim")
        table.add_column("Name")        
        for colour in response_data["data"]:
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
        response = requests.get(f"{url_base}/api/users/part-usage/")
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

@app.command()
def get_possible_sets(user_id: int):
    """
    Get possible sets a user can build from the API.
    """
    try:
        response = requests.get(f"{url_base}/api/user/by-id/{user_id}/possible-sets")
        response.raise_for_status()
        response_data = response.json()
        
        if not response_data["data"]:
            console.print(f"[yellow]No sets can be built by user {user_id}[/yellow]")
            return
        
        for lego_set in response_data["data"]:
            # Set info table
            set_table = Table(show_header=True, header_style="bold magenta")
            set_table.title = f"Set: {lego_set['name']}"
            set_table.add_column("ID", style="dim")
            set_table.add_column("Name")
            set_table.add_column("Total Parts")
            set_table.add_row(
                str(lego_set["id"]),
                lego_set["name"],
                str(len(lego_set["parts"]))
            )
            console.print(set_table)
            
            # Parts table
            parts_table = Table(show_header=True, header_style="bold cyan")
            parts_table.title = "Required Parts"
            parts_table.add_column("Part ID", style="dim")
            parts_table.add_column("Part Name")
            parts_table.add_column("Colour")
            parts_table.add_column("Shape")
            parts_table.add_column("Quantity", justify="right")
            
            for item in lego_set["parts"]:
                part = item["part"]
                parts_table.add_row(
                    str(part["id"]),
                    part["name"],
                    part["colour"]["name"],
                    part["shape"]["name"],
                    str(item["quantity"])
                )
            console.print(parts_table)
            console.print("")  # Empty line between sets
        
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching possible sets: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()