# Flask PostgreSQL Docker Application

This project demonstrates a Flask application with PostgreSQL database, containerized using Docker.

## Project Structure
```
docker_learn/
├── app.py              # Main Flask application
├── database.py         # Database configuration and connection
├── requirements.txt    # Python dependencies
├── Dockerfile         # Instructions for building Docker image
├── docker-compose.yml # Docker services configuration
├── .env              # Environment variables
└── user/             # User module
    ├── models.py     # Database models
    └── routes.py     # API routes
```

## Setup and Installation

### Prerequisites
- Python 3.x
- PostgreSQL
- Docker & Docker Compose

### Local Development Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
PORT=8000
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

4. Run the application:
```bash
python app.py
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## API Endpoints

- GET `/users`: List all users
- POST `/users`: Create a new user
- GET `/users/<id>`: Get user by ID
- PUT `/users/<id>`: Update user by ID
- DELETE `/users/<id>`: Delete user by ID

## Database Configuration

The application uses PostgreSQL with SQLAlchemy ORM. Database connection can be configured through environment variables:

- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `DATABASE_URL`: Full database connection URL

## Development

1. Make sure to activate virtual environment before development
2. Follow PEP 8 style guide for Python code
3. Update requirements.txt when adding new dependencies
4. Use meaningful commit messages following the format:
```
[Author][Project][Day][Description]
``` 