# Personal Notes Manager

## 1. Project Overview

Personal Notes Manager is a web application that allows users to register, log in, and manage their personal notes securely. Each user can access only their own notes.

## 2. Problem Statement

Users need a simple and secure platform to store and access personal notes. The application ensures that notes remain private and that each user can access only their own information.

## 3. Key Features

- User registration and login.
- Secure password hashing.
- JWT access and refresh token authentication.
- View personal notes.
- Create new notes.
- User-specific access to notes.

## 4. Technologies Used

- Python and FastAPI
- SQLite and SQLAlchemy
- React and JavaScript
- JWT Authentication
- Argon2 Password Hashing
- Docker
- GitHub Actions
- AWS EC2

## 5. Database Structure

The application uses SQLite (`notes.db`) with two tables:

**Users:** id, username, email, hashed_password, created_at

**Notes:** id, user_id, title, content, created_at

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a user |
| POST | `/login` | User login |
| POST | `/refresh` | Generate a new access token |
| GET | `/notes` | Retrieve personal notes |
| POST | `/notes` | Create a new note |

## 7. How to Run the Backend

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open API documentation:

http://127.0.0.1:8000/docs

