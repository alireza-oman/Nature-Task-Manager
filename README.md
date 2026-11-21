# Nature Task Manager

A task management web application built with Python and Flask, designed to help users organize and manage their daily tasks efficiently.

The application provides task organization, priority management, filtering, sorting, progress tracking, and CSV export.

## Features

### Authentication
- User registration and login
- Secure password hashing using Werkzeug
- User-specific task management

### Task Management
- Create, edit, complete, and delete tasks
- Pin important tasks
- Assign priorities to tasks
- Organize tasks by category
- Set task due dates

### Search and Organization
- Search tasks
- Filter tasks by status, priority, and category
- Sort tasks by pinned status, due date, and priority

### Additional Features
- Task completion progress tracking
- Export tasks to CSV
- Dark and light theme support
- Responsive user interface
- Persistent theme preference using localStorage

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Flask | Web framework |
| Flask-SQLAlchemy | Database integration |
| SQLAlchemy | Object-relational mapping |
| Jinja2 | Template rendering |
| Werkzeug | Password hashing and security utilities |
| SQLite | Default development database |
| PostgreSQL | Supported database |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Client-side functionality |

## Project Structure

```text
Nature-Task-Manager/
│
├── static/
├── templates/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/alireza-oman/Nature-Task-Manager.git
```

### 2. Navigate to the Project Directory

```bash
cd Nature-Task-Manager
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

The application uses SQLite by default for local development.

To use PostgreSQL, configure the database connection URL:

```env
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

Never commit sensitive configuration values or `.env` files to the repository.

## Usage

Start the Flask application:

```bash
python app.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

Register an account or log in to start managing your tasks.

## Authentication and Data Management

Users can register and log in to access their personal task lists.

Passwords are hashed using Werkzeug before being stored in the database.

Each task is associated with its owner, allowing users to manage their own tasks independently.

## Database

The application uses Flask-SQLAlchemy for database operations.

- SQLite is used by default for local development.
- PostgreSQL is supported through the `DATABASE_URL` environment variable.

## CSV Export

Users can export their tasks as CSV files.

The exported data includes:

- Task ID
- Title
- Description
- Due Date
- Priority
- Category
- Status
- Pinned State

## Theme Support

The application supports both dark and light themes.

The selected theme preference is stored in the browser's `localStorage`, allowing it to persist across page refreshes.

## Author

**Alireza**

- GitHub: [@alireza-oman](https://github.com/alireza-oman)
- Repository: [Nature Task Manager](https://github.com/alireza-oman/Nature-Task-Manager)
