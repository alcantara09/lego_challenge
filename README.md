# LEGO Brick Manager

A LEGO brick inventory API that allows users to track their brick collections and determine which sets they can build.

## Architecture

This project follows **Clean Architecture** principles, ensuring separation of concerns and testability.

```
src/
├── client/                # Primary Adapter - REST API Client
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

### Running the CLI

```bash
# Run any command with:
uv run python -m src.cli.cli <command> [options]

# Get help
uv run python -m src.cli.cli --help
```

#### Available Commands

| Command | Description |
|---------|-------------|
| `extract-db` | Extract the DB from the LEGO API | 
| `get-possible-sets` | Get all possible Sets for brickfan35 |
| `suggest-users`  | Suggest users for part sharing to build tropical-island for landscape-artist. |
| `get-part-usage`  | Get parts that more than 50% of users have.  |
