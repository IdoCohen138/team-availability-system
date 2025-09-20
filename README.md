# Team Availability – FastAPI + React + Postgres


A small full‑stack project that lets team members log in, update their current availability status, and view/filter other teammates' statuses.


**Tech**: FastAPI (Python), Postgres, React (Vite, JS), JWT Auth, Dockerized end‑to‑end. Optional WebSocket for live updates.


## Quick Start (Docker)
1. Copy `.env.example` to `.env` and adjust values if needed.
2. Build & run:
```bash
docker compose up --build
```

## Configuration

### Seed Users Configuration

The system requires a `seed_users.json` file to create initial users. Without this file, you'll get a warning and no users will be created.

#### Option 1: Default File (Recommended)
Create a `seed_users.json` file in the backend directory:
```json
[
  {
    "username": "admin",
    "full_name": "Admin User", 
    "password": "admin123",
    "status": "Working"
  }
]
```

#### Option 2: Custom File Location
Set `SEED_USERS_FILE` environment variable in your `.env` file:
```bash
# Use default file (copied during build)
SEED_USERS_FILE=/app/seed_users.json

# Or point to a custom file (you'll need to mount it)
SEED_USERS_FILE=/app/custom_users.json
```

#### Option 3: Mount Custom File
If you want to use a different file, mount it in `docker-compose.yml`:
```yaml
volumes:
  - ./my_custom_users.json:/app/custom_users.json:ro
```
And set in `.env`:
```bash
SEED_USERS_FILE=/app/custom_users.json
```

**Note**: 
- Container paths start with `/app/`
- Default file is automatically copied during build
- If no seed users configuration is found, the system will show a warning and continue without creating any users.