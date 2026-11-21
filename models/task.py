# models/task.py
from config import get_db_connection

def get_all_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def add_task(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_task(task_id, title):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
        if cursor.fetchone() is None:
            return False
        cursor.execute(
            "UPDATE tasks SET title = %s WHERE id = %s",
            (title, task_id)
        )
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()

def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()

def delete_tasks(task_ids):
    if not task_ids:
        return 0
    placeholders = ", ".join(["%s"] * len(task_ids))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"DELETE FROM tasks WHERE id IN ({placeholders})",
            tuple(task_ids)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()