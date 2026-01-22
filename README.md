# Expense Tracker API

A professional REST API for tracking personal expenses, built with FastAPI and PostgreSQL. This project demonstrates clean architecture principles, proper separation of concerns, and production-ready backend development practices.

## 🎯 Project Overview

This API allows users to manage their personal expenses with features including:
- User authentication with JWT tokens
- Expense categorization
- Date-based filtering and reporting
- Monthly expense summaries
- Category-based analytics

## 🛠️ Technology Stack

### Core Framework
- **FastAPI** - Modern, high-performance web framework for building APIs
- **Python 3.11+** - Programming language
- **Uvicorn** - ASGI server for running the application

### Database
- **PostgreSQL** - Relational database for data persistence
- **SQLAlchemy 2.x** - SQL toolkit and ORM
- **Alembic** - Database migration tool

### Security & Validation
- **JWT (python-jose)** - JSON Web Tokens for authentication
- **Passlib + bcrypt** - Secure password hashing
- **Pydantic** - Data validation and settings management

## 📁 Project Structure

```
expense-tracker/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration scripts
│   ├── env.py                 # Alembic configuration
│   └── script.py.mako         # Migration template
├── app/
│   ├── models/             # SQLAlchemy models (database layer)
│   │   ├── user.py
│   │   ├── category.py
│   │   └── expense.py
│   ├── schemas/           # Pydantic schemas (validation layer)
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── token.py
│   │   └── report.py
│   ├── routers/            # API endpoints (presentation layer)
│   │   ├── auth.py
│   │   ├── categories.py
│   │   ├── expenses.py
│   │   └── reports.py
│   ├── services/              # Business logic (service layer)
│   │   ├── auth_service.py
│   │   ├── category_service.py
│   │   ├── expense_service.py
│   │   └── report_service.py
│   ├── utils/                # Utilities (security, exceptions)
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── config.py              # Application configuration
│   ├── database.py            # Database connection and session
│   ├── dependencies.py        # FastAPI dependencies
│   └── main.py                # Application entry point
├── .env.example               # Environment variables template
├── .gitignore
├── alembic.ini                # Alembic configuration
├── requirements.txt           # Python dependencies
└── README.md
```

## 🏗️ Architecture Principles

### Clean Architecture
The project follows a layered architecture approach:

1. **Presentation Layer** (routers/) - HTTP request/response handling
2. **Service Layer** (services/) - Business logic and use cases
3. **Data Access Layer** (models/) - Database entities and relationships
4. **Validation Layer** (schemas/) - Input/output data validation

### Key Design Decisions

- **Decimal for Money**: Uses `NUMERIC` type for amounts, not floats, ensuring precise decimal arithmetic
- **Dependency Injection**: FastAPI's dependency system for database sessions and authentication
- **Service Pattern**: Business logic separated from API endpoints for better testability
- **Repository Pattern**: Implicit through SQLAlchemy ORM for data access
- **Custom Exceptions**: Centralized error handling with semantic HTTP status codes

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE expense_tracker_db;
   CREATE USER expense_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE expense_tracker_db TO expense_user;
   ```

5. **Configure environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and update with your actual values
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication Flow

1. **Register**: `POST /auth/register` - Create a new user account
2. **Login**: `POST /auth/login` - Receive JWT access token
3. **Use Token**: Include token in Authorization header: `Bearer <token>`

All endpoints except `/auth/register` and `/auth/login` require authentication.

## 📋 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token

### Categories
- `GET /categories` - List all user's categories
- `POST /categories` - Create new category
- `GET /categories/{id}` - Get category by ID
- `DELETE /categories/{id}` - Delete category

### Expenses
- `GET /expenses` - List expenses (with filters: from_date, to_date, category_id)
- `POST /expenses` - Create new expense
- `GET /expenses/{id}` - Get expense by ID
- `DELETE /expenses/{id}` - Delete expense

### Reports
- `GET /reports/monthly?year=2024&month=1` - Monthly expense summary
- `GET /reports/monthly/by-category?year=2024&month=1` - Monthly breakdown by category

## 🔧 Database Migrations

Create a new migration after model changes:
```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback one migration:
```bash
alembic downgrade -1
```

## 🧪 Development

### Generate Secret Key
```bash
openssl rand -hex 32
```

Update the `SECRET_KEY` in your `.env` file with the generated value.

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ RESTful API design principles
- ✅ JWT-based authentication and authorization
- ✅ Proper password hashing with bcrypt
- ✅ Database modeling with relationships (one-to-many)
- ✅ Query optimization with proper indexing
- ✅ Input validation with Pydantic
- ✅ Error handling and custom exceptions
- ✅ Database migrations with Alembic
- ✅ Clean code organization and separation of concerns
- ✅ Dependency injection pattern
- ✅ Environment-based configuration
- ✅ API documentation with OpenAPI/Swagger

## 🚦 Production Considerations

Before deploying to production:

- [ ] Update CORS settings in `main.py` to restrict allowed origins
- [ ] Use strong `SECRET_KEY` (generate with `openssl rand -hex 32`)
- [ ] Set `DEBUG=False` in production environment
- [ ] Use environment variables for all sensitive data
- [ ] Configure proper database connection pooling
- [ ] Add rate limiting middleware
- [ ] Implement comprehensive logging
- [ ] Add health check endpoints for monitoring
- [ ] Consider adding database backups
- [ ] Implement request validation and sanitization
- [ ] Add unit and integration tests

## 📝 License
A clean and extensible Expense Tracker REST API built with FastAPI, PostgreSQL, and SQLAlchemy, focused on real-world backend architecture.

## 👤 Author
@Minells

