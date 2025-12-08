# LEGO Brick Manager

A LEGO brick inventory API that allows users to track their brick collections and determine which sets they can build.

## Architecture

This project follows **Clean Architecture** principles, ensuring separation of concerns and testability.

```
src/
├── api/                   # Primary Adapter - REST API (FastAPI)
│   ├── routers/           # Endpoint definitions
│   ├── dependencies.py    # Dependency injection
│   └── main.py            # FastAPI application
├── cli/                   # Primary Adapter - Command Line Interface
├── domain/                # Core Business Logic (Framework-agnostic)
│   ├── entities/          # Domain models (User, Set, Part, etc.)
│   └── use_cases/         # Business operations
├── ports/                 # Interfaces / Abstractions
│   └── repositories/      # Data access contracts
├── scripts/               # Utility scripts
└── tests/                 # Test suite
    ├── unit/              # Unit Tests
    └── integration/       # Inter dependency testing
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Primary Adapters                       │
│  ┌─────────────────┐          ┌─────────────────────────┐   │
│  │   REST API      │          │         CLI             │   │
│  │  (FastAPI)      │          │       (Typer)           │   │
│  └────────┬────────┘          └───────────┬─────────────┘   │
└───────────┼───────────────────────────────┼─────────────────┘
            │                               │
            ▼                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                           │
│  ┌─────────────────┐          ┌─────────────────────────┐   │
│  │    Entities     │◄────────►│      Use Cases          │   │
│  │ User, Set, Part │          │  AnalyseBuildability    │   │
│  └─────────────────┘          └───────────┬─────────────┘   │
└───────────────────────────────────────────┼─────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         Ports                               │
│                  ┌─────────────────────┐                    │
│                  │  BricksRepository   │ (Interface)        │
│                  └──────────┬──────────┘                    │
└─────────────────────────────┼───────────────────────────────┘
                              │
┌─────────────────────────────┼───────────────────────────────┐
│                   Secondary Adapters                        │
│  ┌──────────────────┐      │      ┌─────────────────────┐   │
│  │ InMemoryRepo     │◄─────┴─────►│   SqlBrickRepo      │   │
│  │ (Testing)        │             │   (Production)      │   │
│  └──────────────────┘             └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## How to run

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/alcantara09/lego_challenge
   cd lego_challenge
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   
   # Or using pip
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. **Initialize the database with basic data**
   ```bash
   python -m src.scripts.initialise_basic_data_in_db
   ```

### Running the API

```bash
# Development mode with auto-reload
uv run fastapi dev src/api/main.py

# Production mode
uv run fastapi run src/api/main.py
```

The API will be available at:
- **API**: http://127.0.0.1:8000
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Running the CLI

```bash
# Run any command with:
uv run python -m src.cli.cli <command> [options]

# Get help
uv run python -m src.cli.cli --help
```

#### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `get-users` | List all users from the API | `uv run python -m src.cli.cli get-users` |
| `get-user-by-id` | Get a user by ID from the API | `uv run python -m src.cli.cli get-user-by-id 1` |
| `get-user-by-name` | Get a user by name from the API | `uv run python -m src.cli.cli get-user-by-name "John"` |
| `get-sets` | List all sets from the API | `uv run python -m src.cli.cli get-sets` |
| `get-set-by-id` | Get a set by ID from the API | `uv run python -m src.cli.cli get-set-by-id 1` |
| `get-set-by-name` | Get a set by name from the API | `uv run python -m src.cli.cli get-set-by-name "Castle"` |
| `get-colours` | List all available colours | `uv run python -m src.cli.cli get-colours` |
| `get-part-usage` | Get parts with usage above a percentage | `uv run python -m src.cli.cli get-part-usage 0.5` |
| `suggest-users` | Suggest users for part sharing | `uv run python -m src.cli.cli suggest-users 1 5` |


## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users |
| GET | `/api/user/by-id/{user_id}` | Get user by ID with full inventory |
| GET | `/api/user/by-name/{name}` | Get user by name |
| GET | `/api/user/by-id/{user_id}/possible-sets` | Get sets user can build |
| GET | `/api/user/by-id/{user_id}/set/{set_id}/suggest-users` | Suggest users for part sharing |

### Sets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sets/` | List all sets |
| GET | `/api/set/by-id/{set_id}` | Get set by ID with parts |
| GET | `/api/set/by-name/{name}` | Get set by name |

### Colours

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/colours/` | List all available colours |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/part-usage?percentage=0.5` | Get parts owned by X% of users |
  