# routes/task_routes.py
import math
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from models.task import add_task, delete_task, delete_tasks, get_all_tasks, update_task
from mysql.connector import Error as MySQLError

task_bp = Blueprint('task', __name__)

ALLOWED_PER_PAGE = (5, 10, 15, 20)


def paginate_tasks(tasks, page, per_page=5):
    total_tasks = len(tasks)
    # Minimal 1 halaman meskipun data di database masih kosong
    total_pages = math.ceil(total_tasks / per_page) if total_tasks > 0 else 1

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start = (page - 1) * per_page
    end = start + per_page
    return tasks[start:end], page, total_pages


@task_bp.route('/')
def index():
    # 1. Ambil pilihan per_page dari URL (default 5)
    per_page = request.args.get('per_page', default=5, type=int)
    if per_page not in ALLOWED_PER_PAGE:
        per_page = 5

    # 2. Ambil halaman saat ini dari URL (default 1)
    page = request.args.get('page', default=1, type=int)

    # 3. Ambil semua tugas dari database
    try:
        tasks = get_all_tasks()
    except MySQLError:
        current_app.logger.exception('Failed to fetch tasks')
        flash('Gagal mengambil data tugas. Silakan coba lagi.', 'error')
        tasks = []

    # 4. Lakukan paginasi
    paginated_tasks, page, total_pages = paginate_tasks(tasks, page, per_page)

    # 5. Render template dengan data yang sudah dipaginasi
    return render_template(
        'index.html',
        tasks=paginated_tasks,
        total_tasks=len(tasks),
        page=page,
        current_page=page,
        total_pages=total_pages,
        per_page=per_page,
        per_page_options=ALLOWED_PER_PAGE,
    )


@task_bp.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    per_page = request.form.get('per_page', default=5, type=int)
    if per_page not in ALLOWED_PER_PAGE:
        per_page = 5

    if not title:
        flash('Tugas tidak boleh kosong.', 'error')
        return redirect(url_for('task.index', per_page=per_page))
    try:
        add_task(title)
    except MySQLError:
        current_app.logger.exception('Failed to add task')
        flash('Tugas gagal ditambahkan. Silakan coba lagi.', 'error')
    else:
        flash('Tugas berhasil ditambahkan.', 'success')
    return redirect(url_for('task.index', per_page=per_page))


@task_bp.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    title = request.form.get('title', '').strip()
    page = request.form.get('page', default=1, type=int)
    per_page = request.form.get('per_page', default=5, type=int)
    if per_page not in ALLOWED_PER_PAGE:
        per_page = 5

    if not title:
        flash('Judul tugas tidak boleh kosong.', 'error')
        return redirect(url_for('task.index', page=page, per_page=per_page))
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
    return redirect(url_for('task.index', page=page, per_page=per_page))


@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    page = request.form.get('page', default=1, type=int)
    per_page = request.form.get('per_page', default=5, type=int)
    if per_page not in ALLOWED_PER_PAGE:
        per_page = 5

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
    return redirect(url_for('task.index', page=page, per_page=per_page))


@task_bp.route('/delete-selected', methods=['POST'])
def delete_selected():
    raw_ids = request.form.getlist('task_ids')
    page = request.form.get('page', default=1, type=int)
    per_page = request.form.get('per_page', default=5, type=int)
    if per_page not in ALLOWED_PER_PAGE:
        per_page = 5

    try:
        task_ids = list(dict.fromkeys(int(task_id) for task_id in raw_ids))
    except ValueError:
        flash('Pilihan tugas tidak valid. Silakan pilih ulang.', 'error')
        return redirect(url_for('task.index', page=page, per_page=per_page))
    if not task_ids:
        flash('Pilih setidaknya satu tugas untuk dihapus.', 'error')
        return redirect(url_for('task.index', page=page, per_page=per_page))
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
    return redirect(url_for('task.index', page=page, per_page=per_page))
