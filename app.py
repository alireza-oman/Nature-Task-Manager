import os
import csv
import io
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, session, flash, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///to_do_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

db = SQLAlchemy(app)


# ----------------- مدل‌های پایگاه داده ----------------- #

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Tasks', backref='owner', lazy=True, cascade="all, delete-orphan")


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='active')  # active, completed
    category = db.Column(db.String(30), default='personal')  # work, personal, study, shopping, fitness
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


with app.app_context():
    db.create_all()


# ----------------- Decorator احراز هویت ----------------- #

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# ----------------- توابع کمکی ----------------- #

def parse_task_date(raw_date):
    if not raw_date:
        return None
    try:
        return datetime.strptime(raw_date.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


# ----------------- مسیرها (Routes) ----------------- #

@app.route('/')
@app.route('/home')
def home():
    if 'user_id' not in session:
        return render_template('home.html', tasks=[], today=date.today(), total_count=0, completed_count=0,
                               progress_percent=0)

    search_word = request.args.get('search', '').strip()
    filter_type = request.args.get('filter', 'all')
    category_filter = request.args.get('category', 'all')
    sort_by = request.args.get('sort', 'pinned')
    current_user_id = session['user_id']

    query = Tasks.query.filter_by(user_id=current_user_id)

    # جستجو
    if search_word:
        query = query.filter(Tasks.title.ilike(f"%{search_word}%"))

    # فیلتر وضعیت یا اولویت
    if filter_type == 'active':
        query = query.filter(Tasks.status == 'active')
    elif filter_type == 'completed':
        query = query.filter(Tasks.status == 'completed')
    elif filter_type == 'high':
        query = query.filter(Tasks.priority == 'high')

    # فیلتر دسته‌بندی
    if category_filter != 'all':
        query = query.filter(Tasks.category == category_filter)

    # مرتب‌سازی (تسک‌های پین‌شده همیشه اولویت اول را دارند)
    if sort_by == 'due_date':
        query = query.order_by(Tasks.is_pinned.desc(), Tasks.date.asc().nullslast())
    elif sort_by == 'priority':
        query = query.order_by(Tasks.is_pinned.desc(), Tasks.priority.desc())
    else:  # پیش‌فرض: جدیدترین‌ها و پین‌شده‌ها
        query = query.order_by(Tasks.is_pinned.desc(), Tasks.id.desc())

    tasks = query.all()

    # محاسبه پیشرفت و آمار
    all_user_tasks = Tasks.query.filter_by(user_id=current_user_id).all()
    total_count = len(all_user_tasks)
    completed_count = sum(1 for t in all_user_tasks if t.status == 'completed')
    progress_percent = int((completed_count / total_count * 100)) if total_count > 0 else 0

    return render_template('home.html',
                           tasks=tasks,
                           today=date.today(),
                           total_count=total_count,
                           completed_count=completed_count,
                           progress_percent=progress_percent)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        raw_date = request.form.get('date', '').strip()
        priority = request.form.get('priority', 'medium')
        category = request.form.get('category', 'personal')
        status = request.form.get('status', 'active')
        is_pinned = bool(request.form.get('is_pinned'))

        if not title:
            flash('Title is required!', 'error')
            return render_template('add_task.html')

        task_date = parse_task_date(raw_date)
        if raw_date and task_date is None:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return render_template('add_task.html')

        task = Tasks(
            title=title,
            description=description,
            date=task_date,
            priority=priority,
            category=category,
            status=status,
            is_pinned=is_pinned,
            user_id=session['user_id']
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_task.html')


@app.route('/toggle_task/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Tasks.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()
    task.status = 'completed' if task.status == 'active' else 'active'
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/toggle_pin/<int:task_id>', methods=['POST'])
@login_required
def toggle_pin(task_id):
    task = Tasks.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()
    task.is_pinned = not task.is_pinned
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/remove_task/<int:task_id>', methods=['POST'])
@login_required
def remove(task_id):
    task = Tasks.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/quick_edit', methods=['POST'])
@login_required
def quick_edit():
    task_id = request.form.get('task_id')
    task = Tasks.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()

    task.title = request.form.get('title', task.title).strip()
    task.priority = request.form.get('priority', task.priority)
    task.category = request.form.get('category', task.category)

    db.session.commit()
    return redirect(url_for('home'))


@app.route('/full_edit/<int:task_id>', methods=['GET'])
@login_required
def full_edit(task_id):
    task = Tasks.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()
    return render_template('edit_task.html', task=task)


@app.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update(task_id):
    task = Tasks.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()

    task.title = request.form.get('title', task.title).strip()
    task.description = request.form.get('description', '').strip()

    raw_date = request.form.get('date', '').strip()
    task_date = parse_task_date(raw_date)
    if raw_date and task_date is None:
        flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
        return render_template('edit_task.html', task=task)

    task.date = task_date
    task.priority = request.form.get('priority', 'medium')
    task.category = request.form.get('category', 'personal')
    task.status = request.form.get('status', 'active')
    task.is_pinned = bool(request.form.get('is_pinned'))

    db.session.commit()
    return redirect(url_for('home'))


@app.route('/export_csv')
@login_required
def export_csv():
    tasks = Tasks.query.filter_by(user_id=session['user_id']).all()
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['ID', 'Title', 'Description', 'Due Date', 'Priority', 'Category', 'Status', 'Pinned'])

    for t in tasks:
        writer.writerow([
            t.id,
            t.title,
            t.description or '',
            t.date.strftime('%Y-%m-%d') if t.date else 'No Date',
            t.priority,
            t.category,
            t.status,
            'Yes' if t.is_pinned else 'No'
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=my_nature_tasks.csv"}
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not password or not email:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if Users.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another one.', 'error')
            return render_template('register.html')

        hashed_pass = generate_password_hash(password, method='pbkdf2:sha256')
        user = Users(username=username, password=hashed_pass, email=email)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember')

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True if remember else False
            return redirect(url_for('home'))

        flash('Invalid username or password!', 'error')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)