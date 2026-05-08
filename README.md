# Task Manager API

A backend Task Management REST API built using FastAPI and SQLAlchemy.

## Features
- Create tasks
- View all tasks
- View single task by ID
- Update tasks
- Delete tasks
- Task priority management
- SQLite database integration
- Interactive API documentation with Swagger UI

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Installation

Clone repository:

```bash
git clone https://github.com/mshahriyarjaved/task-manager-api.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run project:

```bash
python -m uvicorn main:app --reload
```

Open in browser:

```bash
http://127.0.0.1:8000/docs
```

## API Endpoints

### Create Task
POST `/tasks`

### Get All Tasks
GET `/tasks`

### Get Single Task
GET `/tasks/{id}`

### Update Task
PUT `/tasks/{id}`

### Delete Task
DELETE `/tasks/{id}`

## Purpose

This project demonstrates backend development skills including:

- REST API development
- CRUD operations
- Database integration
- FastAPI application structure
- API testing using Swagger UI

## Author

Muhammad Shahriyar  
Python Developer | FastAPI Backend Developer
