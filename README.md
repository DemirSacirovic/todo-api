  # Todo API

  A RESTful API for managing todos with user authentication and authorization.

  **Live Demo**: https://todo-api-demir.onrender.com/docs

  ## Features

  - User registration and authentication (JWT)
  - Secure password hashing
  - User-specific todos (each user sees only their todos)
  - Full CRUD operations
  - SQLite database
  - Interactive API documentation

  ## Tech Stack

  - Python 3.13
  - FastAPI - Web framework
  - SQLAlchemy - Database ORM
  - SQLite - Database
  - JWT - Authentication tokens
  - Passlib + bcrypt - Password hashing
  - Pydantic - Data validation
  - Uvicorn - ASGI server

  ## Installation

  3. Install dependencies
  pip install -r requirements.txt


  1. Clone the repository
  git clone https://github.com/DemirSacirovic/todo-api.git
  cd todo-api

  2. Create virtual environment
  python -m venv venv
  source venv/bin/activate  # Linux/Mac

  ## Running the Application

  uvicorn main:app --reload

  Visit http://localhost:8000/docs for API documentation

  ## API Endpoints

  - GET /todos - Get all todos
  - POST /todos - Create new todo
  - PUT /todos/{id} - Update todo
  - DELETE /todos/{id} - Delete todo

  ## Authentication

  1. Register new user:
  POST /register

  2. Login to get token:
  POST /login

  3. Use token in Authorization header:
  Authorization: Bearer your_jwt_token_here


  ## Database Setup

  The database will be created automatically when you first run the application.
  SQLite file: `todos.db`
