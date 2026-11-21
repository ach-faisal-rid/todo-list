# routes/task_routes.py
from flask import Blueprint, current_app, flash, redirect, render_template, request
from mysql.connector import Error as MySQLError
from models.task import add_task, delete_task, delete_tasks, get_all_tasks, update_task

task_bp = Blueprint('task', __name__)

@task_bp.route('/')
def index():
    tasks = get_all_tasks()
    return render_template('index.html', tasks=tasks)

@task_bp.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Tugas tidak boleh kosong.', 'error')
        return redirect('/')
    try:
        add_task(title)
    except MySQLError:
        current_app.logger.exception('Failed to add task')
        flash('Tugas gagal ditambahkan. Silakan coba lagi.', 'error')
    else:
        flash('Tugas berhasil ditambahkan.', 'success')
    return redirect('/')

@task_bp.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    title = request.form.get('title', '').strip()
    if not title:
        flash('Judul tugas tidak boleh kosong.', 'error')
        return redirect('/')
    try:
        updated = update_task(task_id, title)
    except MySQLError:
        current_app.logger.exception('Failed to edit task %s', task_id)
        flash('Tugas gagal diedit. Silakan coba lagi.', 'error')
    else:
        if updated:
            flash('Tugas berhasil diedit.', 'success')
        else:
            flash('Tugas yang ingin diedit tidak ditemukan.', 'error')
    return redirect('/')

@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    try:
        deleted = delete_task(task_id)
    except MySQLError:
        current_app.logger.exception('Failed to delete task %s', task_id)
        flash('Tugas gagal dihapus. Silakan coba lagi.', 'error')
    else:
        if deleted:
            flash('Tugas berhasil dihapus.', 'success')
        else:
            flash('Tugas yang ingin dihapus tidak ditemukan.', 'error')
    return redirect('/')

@task_bp.route('/delete-selected', methods=['POST'])
def delete_selected():
    raw_ids = request.form.getlist('task_ids')
    try:
        task_ids = list(dict.fromkeys(int(task_id) for task_id in raw_ids))
    except ValueError:
        flash('Pilihan tugas tidak valid. Silakan pilih ulang.', 'error')
        return redirect('/')
    if not task_ids:
        flash('Pilih setidaknya satu tugas untuk dihapus.', 'error')
        return redirect('/')
    try:
        deleted_count = delete_tasks(task_ids)
    except MySQLError:
        current_app.logger.exception('Failed to delete selected tasks')
        flash('Tugas yang dipilih gagal dihapus. Silakan coba lagi.', 'error')
    else:
        if deleted_count:
            flash(f'{deleted_count} tugas berhasil dihapus.', 'success')
        else:
            flash('Tugas yang dipilih tidak ditemukan.', 'error')
    return redirect('/')
