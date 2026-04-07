# AGENTS.md - PredictMatch Coding Guidelines

PredictMatch is a football match prediction app with FastAPI backend and React frontend.

## Project Structure

```
app/                 # Python FastAPI backend
├── api/routes/      # API endpoints
├── services/        # Business logic
├── db/              # Database models & repositories
├── config/          # Settings & logging
├── ml/              # Machine learning models
├── jobs/            # Background tasks
└── utils/           # Utilities

frontend/            # React web interface
├── src/components/  # UI components (home/, layout/, ui/)
├── src/pages/       # Page components
├── src/services/    # API client functions
└── public/          # Static assets

tests/               # Test suites
├── test_api/
├── test_services/
├── test_jobs/
└── test_ml/

notebooks/           # Jupyter experiments
scripts/             # Utility scripts
```

## Commands

### Backend (Python)
```bash
# Start development server
uvicorn app.main:app --reload

# Run all tests
pytest

# Run single test file
pytest tests/test_api/test_matches.py

# Run single test
pytest tests/test_api/test_matches.py::test_get_matches

# Run with coverage
pytest --cov=app --cov-report=html

# Linting (install ruff/black if needed)
ruff check app/
ruff format app/
```

### Frontend (React)
```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint

# Preview production build
npm run preview
```

## Python Code Style

### Imports
- Order: stdlib → third-party → local
- Group with blank lines between sections
- Use absolute imports within `app/`

```python
import os
from datetime import datetime

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

from app.services.match_service import MatchService
from app.db.repositories.match_repository import MatchRepository
```

### Naming Conventions
- Classes: `PascalCase` (e.g., `MatchService`, `PredictionModel`)
- Functions/variables: `snake_case` (e.g., `get_matches`, `match_id`)
- Constants: `UPPER_SNAPE_CASE` (e.g., `FOOTBALL_DATA_API_KEY`)
- Private: `_leading_underscore` (e.g., `_normalize_data`)

### Type Hints
- Use type hints for function signatures
- Use `|` for unions (Python 3.10+): `str | None`
- Return types: `-> dict`, `-> list[Match]`

```python
def get_matches(
    competition_code: str | None = None,
    date_from: str | None = None
) -> dict:
    ...
```

### Error Handling
- API routes: catch exceptions, raise `HTTPException`
- Services: let exceptions bubble up or return Result types
- Always log errors before raising

```python
from fastapi import HTTPException

@router.get("/matches/")
def get_matches():
    try:
        return service.get_matches()
    except Exception as e:
        logger.error(f"Failed to fetch matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Classes
- Use dataclasses for data models (if needed)
- Explicit `__init__` with type hints
- Service classes instantiate dependencies in `__init__`

```python
class MatchService:
    def __init__(self) -> None:
        self.client = FootballDataClient()
    
    def get_matches(self, ...) -> dict:
        ...
```

## JavaScript/React Code Style

### Imports
- Group: React → third-party → local
- Use relative imports with `./` or `../`

```javascript
import { useEffect, useState } from "react";

import Header from "../components/layout/Header";
import { fetchCompetitions } from "../services/api";
```

### Naming Conventions
- Components: `PascalCase` (e.g., `HomePage`, `MatchCard`)
- Functions/variables: `camelCase` (e.g., `fetchMatches`, `selectedLeague`)
- Constants: `UPPER_SNAKE_CASE` for true constants
- Files: `PascalCase.jsx` for components, `camelCase.js` for utilities

### Component Structure
- Functional components with hooks
- Props destructuring in parameters
- Early returns for loading/error states

```javascript
function MatchesSection({ matches, onAnalyzeMatch }) {
  if (!matches.length) return <p>No matches found</p>;
  
  return (
    <section>
      {matches.map(match => (
        <MatchCard key={match.id} match={match} />
      ))}
    </section>
  );
}
```

### Formatting
- 2-space indentation
- Double quotes for strings
- Semicolons required
- Trailing commas in multi-line objects/arrays
- Max line length: 88-100 characters

### Error Handling
- Async functions: try/catch with console.error
- API calls: throw errors to be caught by caller

```javascript
async function loadCompetitions() {
  try {
    const data = await fetchCompetitions();
    setCompetitions(data.competitions || []);
  } catch (error) {
    console.error("Failed to load competitions:", error);
  }
}
```

## Testing

### Python Tests
- Use pytest
- Test files: `test_*.py`
- Test functions: `test_*` with descriptive names
- Use fixtures for shared setup
- Mock external API calls

```python
def test_get_matches_returns_list():
    service = MatchService()
    result = service.get_matches()
    assert "matches" in result
    assert isinstance(result["matches"], list)
```

### Frontend Testing
- Add Jest/Vitest for unit tests
- Add React Testing Library for component tests
- Test files: `*.test.jsx` or `*.spec.jsx`

## Environment Configuration

- Use `.env` file (see `.env.example`)
- Load with `python-dotenv` in settings
- Never commit `.env` or secrets
- Frontend: use `import.meta.env` for Vite env vars

## Git Workflow

- Main branch: `main`
- Feature branches: `feature/description`
- Commit messages: present tense, descriptive
- Run `npm run lint` before committing frontend changes
- Run `pytest` before committing backend changes

## External APIs

- football-data.org API for match data
- Handle rate limits gracefully
- Cache responses when appropriate
- Respect API terms of service
