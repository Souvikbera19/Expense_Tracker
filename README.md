# 💸 Expense Tracker API

A lightweight, high-performance Expense Tracker API built with **FastAPI**, **SQLite**, and **Pydantic**. This application allows users to record daily expenses, categorize them, query list of expenses, and track total expenditures.

---

## 🚀 Features

- **Add Expense**: Record new expenses with amount, category, and description.
- **List Expenses**: View a complete history of all recorded expenses.
- **Total Expenditure**: Instantly calculate the sum of all recorded expenses.
- **Auto-Initialization**: Automatic SQLite database schema setup on application start.
- **Interactive Documentation**: Built-in Swagger and ReDoc interactive API exploratory playgrounds.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database**: SQLite (via standard Python `sqlite3`)
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Fast Python package installer and resolver)

---

## 📁 Project Structure

```text
expense_tracker/
├── app/
│   ├── app.py          # FastAPI application routes and logic
│   ├── databse.py      # SQLite database configuration and initialization
│   ├── schemas.py      # Pydantic data schemas/models
│   └── expenses.db     # SQLite database file (created automatically)
├── main.py             # Uvicorn entry point
├── pyproject.toml      # Dependency & project configuration
├── uv.lock             # uv lockfile for deterministic builds
└── README.md           # Project documentation (this file)
```

---

## ⚡ Quick Start

### Prerequisites

- Python `>= 3.13`
- `uv` installed (`pip install uv` or via curl/brew)

### 1. Installation

Clone the repository and install the dependencies:

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
Once the server is running, you can explore the endpoints interactively via:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### Endpoints Reference

#### 1. Home / Root
* **Endpoint**: `GET /`
* **Description**: Simple API health check and welcome message.
* **Response**:
  ```json
  {
    "message": "Welcome to expense tracker"
  }
  ```

#### 2. Add an Expense
* **Endpoint**: `POST /AddExpense`
* **Description**: Records a new expense.
* **Request Body** (JSON):
  > [!IMPORTANT]
  > Note that the JSON body expects `desc` for the description field, which maps to `description` in the database.
  
  ```json
  {
    "amount": 42.50,
    "category": "Food",
    "desc": "Lunch at diner"
  }
  ```
* **Response**: `200 OK` (with no response body on success)

#### 3. Get All Expenses
* **Endpoint**: `GET /expenses`
* **Description**: Retrieves all recorded expenses from the database.
* **Response**:
  ```json
  [
    [
      42.50,
      "Food",
      "Lunch at diner",
      "2026-06-24T22:52:00.123456"
    ]
  ]
  ```

#### 4. Get Total Expenditure
* **Endpoint**: `GET /TotalExpenses`
* **Description**: Calculates the sum of all expenses.
* **Response**:
  ```json
  42.50
  ```

---

## 🗄️ Database Schema

The database (`expenses.db`) contains a single table `expenses` structured as follows:

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `amount` | `REAL` | `NOT NULL` | The monetary value of the expense |
| `category` | `TEXT` | `NOT NULL` | Category of the expense (e.g., Food, Travel) |
| `description` | `TEXT` | | Optional notes (populated from `desc` in requests) |
| `created_at` | `TEXT` | | ISO-8601 string of when the expense was added |
