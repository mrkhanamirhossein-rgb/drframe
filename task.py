import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"

def init_task_db():
    """Initialize the tasks table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                importance INTEGER DEFAULT 1,
                is_done INTEGER DEFAULT 0
            );'''
        )
        conn.commit()

def add_task(username, title, description="", deadline=None, importance=1):
    """Add a new task for a user."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO tasks (username, title, description, deadline, importance) VALUES (?, ?, ?, ?, ?)",
            (username, title, description, deadline, importance)
        )
        conn.commit()
    print(f"[DEBUG] Added task for {username}: {title} - {description} (Deadline: {deadline}, Importance: {importance})")

def list_tasks(username):
    """List all tasks for a user, both done and undone."""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, description, deadline, importance, is_done FROM tasks WHERE username=? ORDER BY is_done ASC, importance DESC, deadline ASC",
            (username,)
        )
        rows = cur.fetchall()
    tasks = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "deadline": row[3],
            "importance": row[4],
            "is_done": bool(row[5])
        }
        for row in rows
    ]
    return tasks

def get_task(username, task_id):
    """Get a single task by id for a user."""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, description, deadline, importance, is_done FROM tasks WHERE username=? AND id=?",
            (username, task_id)
        )
        row = cur.fetchone()
    if row:
        task = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "deadline": row[3],
            "importance": row[4],
            "is_done": bool(row[5])
        }
        return task
    return None

def update_task(username, task_id, title=None, description=None, deadline=None, importance=None):
    """Update a task's details."""
    with sqlite3.connect(DB_NAME) as conn:
        updates = []
        params = []
        if title is not None:
            updates.append("title=?")
            params.append(title)
        if description is not None:
            updates.append("description=?")
            params.append(description)
        if deadline is not None:
            updates.append("deadline=?")
            params.append(deadline)
        if importance is not None:
            updates.append("importance=?")
            params.append(importance)
        
        if updates:
            query = f"UPDATE tasks SET {', '.join(updates)} WHERE username=? AND id=?"
            params.extend([username, task_id])
            conn.execute(query, params)
            conn.commit()

def set_task_done(username, task_id, done=True):
    """Mark a task as done or undone."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE tasks SET is_done=? WHERE username=? AND id=?",
            (1 if done else 0, username, task_id)
        )
        conn.commit()
    print(f"[DEBUG] set_task_done for {username}, id={task_id}: done={done}")

def delete_task(username, task_id):
    """Delete a task by id for a user."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "DELETE FROM tasks WHERE username=? AND id=?",
            (username, task_id)
        )
        conn.commit()
    print(f"[DEBUG] delete_task for {username}, id={task_id}")