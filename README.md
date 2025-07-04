# Book Review Service

A high-performance backend service for managing books and their reviews — built using **Python**, **FastAPI**, **SQLAlchemy**, **Redis**, and **Alembic**. This project demonstrates clean API design, database modeling, migrations, indexing, caching, testing, and scalability fundamentals.

---

## 🚀 Features

- **Book Management** - Add & retrieve books with validation
- **Review System** - Add & fetch reviews for books  
- **Redis Caching** - High-performance caching with fallback logic
- **API Documentation** - Interactive Swagger UI via FastAPI
- **Database Migrations** - Version-controlled schema with Alembic
- **Performance Optimization** - Database indexing for fast queries
- **Comprehensive Testing** - Unit & integration test coverage
- **Production Ready** - SQLite/PostgreSQL support with ORM

---

## 🛠️ Tech Stack

| Layer         | Tools Used                                |
|---------------|-------------------------------------------|
| Language      | Python 3.11+                             |
| Framework     | FastAPI                                   |
| ORM           | SQLAlchemy                                |
| Database      | SQLite (PostgreSQL compatible)           |
| Migrations    | Alembic                                   |
| Caching       | Redis (via `redis.asyncio`)              |
| Testing       | Pytest + httpx + pytest-asyncio          |
| Documentation | Swagger UI (`/docs`)                      |

---

## Getting Started

### Clone the Repository

```bash
git clone <your-repo-url>
cd Book-Review-Service
```

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv myenv

# Activate environment
# Windows:
myenv\Scripts\activate
# Mac/Linux:
source myenv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages in `requirements.txt`:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
redis==5.0.1
pytest==7.4.3
httpx==0.25.2
pytest-asyncio==0.21.1
pydantic==2.5.0
```

### Setup Redis Server

Ensure Redis is installed and running locally on port `6379`.

**For Windows users:**
- Download Redis from [Microsoft Archive](https://github.com/microsoftarchive/redis/releases)
- Run: `redis-server.exe`

**For Mac users:**
```bash
brew install redis
brew services start redis
```

**For Linux users:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### Database Setup & Migrations

#### Initialize Alembic (First time only)

```bash
# Initialize alembic configuration
alembic init alembic
```

#### Configure Alembic

1. **Update `alembic.ini`:**
```ini
sqlalchemy.url = sqlite:///./books.db
```

2. **Update `alembic/env.py` (add at the top):**
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.database import Base
from app import models
```

3. **Update target_metadata in `alembic/env.py`:**
```python
# Replace: target_metadata = None
# With:
target_metadata = Base.metadata
```

#### Run Database Migrations

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial schema with books and reviews"

# Apply migrations
alembic upgrade head

# Generate index migration
alembic revision --autogenerate -m "Add index on reviews.book_id"
alembic upgrade head
```

### Start the Application

```bash
uvicorn app.main:app --reload
```

**Access Points:**
- **API Base**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Database Migrations Guide

### Understanding Alembic Workflow

Alembic provides version control for your database schema:

```bash
# Check current migration status
alembic current

# View migration history
alembic history --verbose

# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

### Database Schema

The service uses two main tables with optimized indexing:

**Books Table:**
- `id` (Primary Key, Auto-increment)
- `title` (String, Required)
- `author` (String, Required)  
- `description` (Text, Optional)

**Reviews Table:**
- `id` (Primary Key, Auto-increment)
- `content` (Text, Required)
- `book_id` (Foreign Key → books.id, **Indexed**)

**Performance Optimization:**
- Index on `reviews.book_id` for fast review lookups by book
- Foreign key constraints for data integrity

### Switching to PostgreSQL

To use PostgreSQL instead of SQLite:

1. **Install PostgreSQL driver:**
```bash
pip install psycopg2-binary
```

2. **Update `app/database.py`:**
```python
DATABASE_URL = "sqlite:///./books.db"
```

3. **Update `alembic.ini`:**
```ini
sqlalchemy.url = sqlite:///./books.db
```

---

## Running Tests

### Test Configuration

```bash
# Set Python path (Windows)
$env:PYTHONPATH = "."

# Set Python path (Mac/Linux)  
export PYTHONPATH="."
```

### Execute Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_books.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage

The test suite includes:

- **Unit Tests** - `test_get_books`, `test_add_book`
- **Integration Tests** - `test_cache_miss`, `test_redis_fallback`
- **API Tests** - End-to-end endpoint testing
- **Database Tests** - Migration and model validation

---

## Project Structure

```
Book-Review-Service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # Database configuration & connection
│   ├── cache.py            # Redis caching logic
│   └── routers/
│       ├── __init__.py
│       ├── books.py         # Book-related API endpoints
│       └── reviews.py       # Review-related API endpoints
├── tests/
│   ├── __init__.py
│   ├── test_books.py        # Book API tests
│   ├── test_reviews.py      # Review API tests
│   └── test_cache.py        # Cache integration tests
├── alembic/
│   ├── versions/            # Migration files
│   ├── env.py              # Alembic environment configuration
│   └── script.py.mako      # Migration template
├── alembic.ini             # Alembic configuration
├── requirements.txt        # Python dependencies
├── books.db               # SQLite database file (generated)
└── README.md              # This file
```

---

## API Endpoints

### Books

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/books/` | Get all books with caching |
| `POST` | `/books/` | Create a new book |
| `GET` | `/books/{book_id}` | Get book by ID |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/books/{book_id}/reviews/` | Get all reviews for a book |
| `POST` | `/books/{book_id}/reviews/` | Add review to a book |

### Example API Usage

```bash
# Add a book
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{"title": "The Alchemist", "author": "Paulo Coelho", "description": "A philosophical novel"}'

# Get all books
curl -X GET "http://localhost:8000/books/"

# Add a review
curl -X POST "http://localhost:8000/books/1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"content": "Amazing book with deep philosophical insights!"}'

# Get reviews for a book
curl -X GET "http://localhost:8000/books/1/reviews/"
```

---

## Design Decisions & Architecture

### Caching Strategy

| Scenario | Behavior |
|----------|----------|
| **Cache Hit** | Return data directly from Redis (⚡ Fast) |
| **Cache Miss** | Fetch from DB → Store in Redis → Return data |
| **Redis Down** | Graceful fallback to database only |
| **Cache TTL** | 300 seconds (5 minutes) for book lists |

### Database Design Choices

| Decision | Rationale |
|----------|-----------|
| **SQLAlchemy ORM** | Type safety, relationship management, migration support |
| **Alembic Migrations** | Version control for database schema changes |
| **Index on book_id** | O(log n) lookup for reviews instead of O(n) table scan |
| **Foreign Key Constraints** | Data integrity and referential consistency |

### Error Handling

- **404 Not Found** - Book/Review doesn't exist
- **422 Validation Error** - Invalid request data format
- **500 Internal Server Error** - Database/Redis connection issues
- **Graceful Degradation** - Service continues without cache if Redis fails

---

## Production Considerations & Scaling

### Immediate Improvements

| Area | Enhancement | Implementation |
|------|-------------|----------------|
| **Authentication** | JWT-based auth | Add user roles (reader/admin) |
| **Rate Limiting** | API throttling | Use slowAPI or nginx rate limiting |
| **Logging** | Structured logging | Add request tracing and metrics |
| **Monitoring** | Health checks | Add `/health` and `/metrics` endpoints |

### Scaling Strategy

| Component | Current | Scaled Version |
|-----------|---------|----------------|
| **Database** | SQLite | PostgreSQL with read replicas |
| **Cache** | Single Redis | Redis Cluster with sharding |
| **API** | Single instance | Load-balanced with Docker/K8s |
| **Search** | DB queries | Elasticsearch for full-text search |

### Advanced Features

- **GraphQL Support** - Use Strawberry for flexible queries
- **Real-time Updates** - WebSocket notifications for new reviews  
- **Content Moderation** - ML-based review sentiment analysis
- **Recommendation Engine** - Suggest books based on review patterns

### License

This project is licensed under the [MIT License](./LICENSE).  
© 2025 Chirag Gupta. Please credit if reused.
