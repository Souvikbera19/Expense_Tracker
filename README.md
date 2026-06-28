# 💸 Expense Tracker API

A lightweight, secure, and high-performance Expense Tracker API built with **FastAPI**, **SQLite**, and **Pydantic**. The application supports multi-user registration, secure JWT authentication, and isolated expense tracking per user.

---

## 🚀 Features

- **User Registration**: Register new accounts securely.
- **JWT Authentication**: Secure login endpoints providing token-based authentication (OAuth2 password flow).
- **Add Expense**: Record new expenses with amount, category, description, and auto-populated timestamps, fully isolated per user.
- **List Expenses**: View history of expenses matching the logged-in user.
- **Total Expenditure**: Instantly calculate the sum of all expenses recorded by the logged-in user.
- **Auto-Initialization**: Automatic SQLite database creation and schema setup on application start.
- **Interactive Documentation**: Built-in Swagger and ReDoc interactive API playgrounds.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Security & Authentication**: OAuth2, JWT (`pyjwt`), and Argon2 password hashing (`pwdlib[argon2]`)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database**: SQLite (via standard Python `sqlite3`)
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Fast Python package installer and resolver)

---

## 📁 Project Structure

```text
expense_tracker/
├── app/
│   ├── app.py          # FastAPI application routes and endpoints
│   ├── auth.py         # Authentication logic (JWT, password verification, user dependencies)
│   ├── databse.py      # SQLite database configuration, row factory, and initialization
│   └── schemas.py      # Pydantic schemas (Expense, User, UserRegister, etc.)
├── main.py             # Uvicorn entry point
├── pyproject.toml      # Dependency & project configuration
├── uv.lock             # uv lockfile for deterministic builds
├── database.db         # SQLite database file (created automatically in the project root)
└── README.md           # Project documentation (this file)
```

---

## ⚡ Quick Start

### Prerequisites

- Python `>= 3.13`
- `uv` installed (`pip install uv` or via curl/brew)

### 1. Installation

Clone the repository and install all dependencies:

```bash
# Sync/install all dependencies into the virtual environment
uv sync
```

### 2. Run the Server

Start the development server with hot-reload enabled:

```bash
uv run main.py
```

The server will run locally at `http://127.0.0.1:8000`.

---

## 📖 API Endpoints & Usage

### Interactive API Docs
Once the server is running, you can explore and test the endpoints interactively via:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### Endpoints Reference

#### 1. Home / Root
* **Endpoint**: `GET /`
* **Description**: Simple API health check.
* **Response**:
  ```json
  {
    "message": "Welcome to expense tracker"
  }
  ```

#### 2. Register User
* **Endpoint**: `POST /register`
* **Description**: Register a new user.
* **Request Body** (JSON):
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123",
    "email": "johndoe@example.com",
    "full_name": "John Doe"
  }
  ```
* **Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "full_name": "John Doe"
  }
  ```

#### 3. Log In / Obtain Token
* **Endpoint**: `POST /token`
* **Description**: Logs in a user and returns a JWT token. Form data (OAuth2 standard) is required.
* **Request Body** (Form Data):
  - `username`: `johndoe`
  - `password`: `securepassword123`
* **Response** (`200 OK`):
  ```json
  {
    "access_token": "eyJhbGciOiJIUz...",
    "token_type": "bearer"
  }
  ```

#### 4. Get Current User Profile
* **Endpoint**: `GET /users/me`
* **Authentication**: Bearer token required.
* **Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "full_name": "John Doe",
    "disabled": null
  }
  ```

#### 5. Add an Expense
* **Endpoint**: `POST /AddExpense`
* **Authentication**: Bearer token required.
* **Description**: Records a new expense associated with the authenticated user.
* **Request Body** (JSON):
  ```json
  {
    "amount": 42.50,
    "category": "Food",
    "desc": "Lunch at diner"
  }
  ```
* **Response** (`200 OK`):
  ```json
  {
    "message": "Expense added successfully"
  }
  ```

#### 6. Get All User Expenses
* **Endpoint**: `GET /expenses`
* **Authentication**: Bearer token required.
* **Description**: Retrieves all expenses associated with the authenticated user.
* **Response** (`200 OK`):
  ```json
  [
    {
      "amount": 42.50,
      "category": "Food",
      "description": "Lunch at diner",
      "created_at": "2026-06-28T12:06:20.541765"
    }
  ]
  ```

#### 7. Get Total Expenditure
* **Endpoint**: `GET /TotalExpenses`
* **Authentication**: Bearer token required.
* **Description**: Calculates the sum of all expenses belonging to the authenticated user.
* **Response** (`200 OK`):
  ```json
  42.50
  ```

---

## 🗄️ Database Schema

The database (`database.db`) is automatically initialized with two tables:

### 1. `users` Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the user |
| `username` | `VARCHAR(50)` | `NOT NULL UNIQUE` | Unique username |
| `email` | `VARCHAR(50)` | `NOT NULL` | User email address |
| `full_name` | `VARCHAR(50)` | `NOT NULL` | User's full name |
| `hashed_password` | `TEXT` | `NOT NULL` | Hashed user password |

### 2. `expenses` Table
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `amount` | `REAL` | `NOT NULL` | Monetary value of the expense |
| `category` | `TEXT` | `NOT NULL` | Category of the expense |
| `description` | `TEXT` | | Description/note |
| `created_at` | `TEXT` | | Timestamp of creation (ISO-8601) |
| `user_id` | `INTEGER` | `REFERENCES users(id)` | Foreign key identifying the expense owner |
