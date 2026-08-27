# 🌲 Nature Task Manager

A modern and responsive **To-Do List web application** built with **Flask** and **Flask-SQLAlchemy**.

Nature Task Manager helps users organize their daily tasks with authentication, priorities, categories, due dates, filtering, sorting, progress tracking, and CSV export.

## ✨ Features

* 🔐 User registration and login
* 🔒 User-specific task management
* ✅ Create, edit, complete, and delete tasks
* 📌 Pin important tasks
* 🎯 Set task priority
* 🗂️ Organize tasks by category
* 📅 Set due dates
* 🔎 Search tasks
* 🔽 Filter tasks by status, priority, and category
* 🔃 Sort tasks by pinned status, due date, or priority
* 📊 Track task completion progress
* 📥 Export tasks to CSV
* 🌙 Dark / Light mode
* 🔑 Secure password hashing with Werkzeug
* 📱 Responsive interface

## 🛠️ Technologies

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **SQLAlchemy**
* **Jinja2**
* **Werkzeug**
* **SQLite** for local development
* **PostgreSQL** support
* **HTML5**
* **CSS3**
* **JavaScript**

## 📁 Project Structure

```text
To-Do-List/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── add_task.html
│   └── edit_task.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
cd To-Do-List
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

The application uses SQLite by default for local development.

To use PostgreSQL, set the database connection URL:

```env
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

Sensitive values such as `.env` should never be committed to GitHub.

## ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 🔐 Authentication

Users can create an account and log in to manage their personal tasks.

Passwords are securely hashed using Werkzeug before being stored in the database.

Each task is associated with its owner, preventing users from accessing or modifying other users' tasks.

## 📊 Task Management

Each task can contain:

* Title
* Description
* Category
* Priority
* Due date
* Status
* Pinned state
* Creation date

## 🗃️ Database

The application uses **Flask-SQLAlchemy** as the ORM.

SQLite is used for local development, while the application is also prepared to work with PostgreSQL through the `DATABASE_URL` environment variable.

## 📥 CSV Export

Users can export their tasks as a CSV file containing:

```text
ID
Title
Description
Due Date
Priority
Category
Status
Pinned
```

## 🌙 Theme

The application includes a Dark / Light mode toggle.

The selected theme is stored in the browser's `localStorage`, so the preference remains after refreshing the page.
