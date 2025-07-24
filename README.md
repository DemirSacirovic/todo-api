  # TODO API

  Simple REST API built with FastAPI for managing todo items.

  ## Features

  - Create new todos
  - Get all todos
  - Update existing todos
  - Delete todos

  ## Tech Stack

  - Python 3.13
  - FastAPI
  - Pydantic
  - Uvicorn

  ## Installation

  1. Clone the repository
  git clone https://github.com/DemirSacirovic/todo-api.git
  cd todo-api

  2. Create virtual environment
  python -m venv venv
  source venv/bin/activate  # Linux/Mac

  3. Install dependencies
  pip install fastapi uvicorn

  ## Running the Application

  uvicorn main:app --reload

  Visit http://localhost:8000/docs for API documentation

  ## API Endpoints

  - GET /todos - Get all todos
  - POST /todos - Create new todo
  - PUT /todos/{id} - Update todo
  - DELETE /todos/{id} - Delete todo
