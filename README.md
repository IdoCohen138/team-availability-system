# Team Availability – FastAPI + React + Postgres


A small full‑stack project that lets team members log in, update their current availability status, and view/filter other teammates' statuses.


**Tech**: FastAPI (Python), Postgres, React (Vite, JS), JWT Auth, Dockerized end‑to‑end. Optional WebSocket for live updates.


## Quick Start (Docker)

**Prerequisites**: Make sure you have Docker and Docker Compose installed on your system.
- [Download Docker Desktop](https://docs.docker.com/get-docker/)

1. Create a `.env` file with the required environment variables (see Configuration section below).
2. Create a `seed_users.json` file in the backend directory (see Seed Users Configuration below).
3. Build & run:
```bash
docker compose up --build
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Database Configuration
POSTGRES_DB=team_availability
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# JWT Authentication
JWT_SECRET=your_jwt_secret_key_here

# Application Settings
SEED=1
CORS_ORIGINS=http://localhost:5173

# Frontend API URL
VITE_API_BASE_URL=http://localhost:8000
```

**Environment Variables Explanation:**
- `POSTGRES_DB`: Database name for the PostgreSQL instance
- `POSTGRES_USER`: Username for PostgreSQL authentication
- `POSTGRES_PASSWORD`: Password for PostgreSQL authentication
- `JWT_SECRET`: Secret key for JWT token generation (use a strong, random string)
- `SEED`: Set to 1 to enable database seeding, 0 to disable
- `CORS_ORIGINS`: Allowed origins for CORS (comma-separated if multiple)
- `VITE_API_BASE_URL`: Backend API URL for the frontend to connect to

### Seed Users Configuration

The system requires a `seed_users.json` file to create initial users. Without this file, you'll get a warning and no users will be created.

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

**Note**: 
- The default file is automatically copied during build
- If no seed users configuration is found, the system will show a warning and continue without creating any users