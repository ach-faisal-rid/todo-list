const taskCheckboxes = [...document.querySelectorAll('.task-checkbox')];
const selectAll = document.querySelector('#select-all');
const selectionCount = document.querySelector('#selection-count');

function updateSelection() {
    const selectedCount = taskCheckboxes.filter((checkbox) => checkbox.checked).length;
    selectionCount.textContent = selectedCount
        ? `${selectedCount} tugas dipilih`
        : 'Belum ada tugas dipilih';
    selectAll.checked = taskCheckboxes.length > 0 && selectedCount === taskCheckboxes.length;
    selectAll.indeterminate = selectedCount > 0 && selectedCount < taskCheckboxes.length;
}

selectAll.addEventListener('change', () => {
    taskCheckboxes.forEach((checkbox) => {
        checkbox.checked = selectAll.checked;
    });
    updateSelection();
});
taskCheckboxes.forEach((checkbox) => checkbox.addEventListener('change', updateSelection));

const editDialog = document.querySelector('.edit-dialog');
const editTaskForm = document.querySelector('#edit-task-form');
const editTaskTitle = document.querySelector('#edit-task-title');

document.querySelectorAll('.task-edit-trigger').forEach((button) => {
    button.addEventListener('click', () => {
        editTaskForm.action = button.dataset.editUrl;
        editTaskTitle.value = button.dataset.taskTitle;
        editDialog.showModal();
        editTaskTitle.focus();
        editTaskTitle.select();
    });
});
document.querySelector('.edit-dialog-close').addEventListener('click', () => editDialog.close());
document.querySelector('.edit-dialog-cancel').addEventListener('click', () => editDialog.close());
editDialog.addEventListener('click', (event) => {
    if (event.target === editDialog) {
        editDialog.close();
    }
});

const deleteConfirmation = document.querySelector('#delete-confirmation');
const deleteConfirmationMessage = document.querySelector('#delete-confirmation-message');
const cancelDelete = document.querySelector('#cancel-delete');
const confirmDelete = document.querySelector('#confirm-delete');
let pendingDeleteForm = null;
let confirmedDeleteForm = null;

function closeDeleteConfirmation() {
    deleteConfirmation.hidden = true;
    pendingDeleteForm = null;
}

document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', (event) => {
        if (!form.matches('.delete-form, #bulk-delete-form')) {
            return;
        }

        if (form === confirmedDeleteForm) {
            confirmedDeleteForm = null;
            return;
        }

        if (form.id === 'bulk-delete-form' && !taskCheckboxes.some((checkbox) => checkbox.checked)) {
            return;
        }

        event.preventDefault();
        pendingDeleteForm = form;
        deleteConfirmationMessage.textContent = form.id === 'bulk-delete-form'
            ? 'Yakin ingin menghapus semua tugas yang dipilih?'
            : event.submitter?.dataset.confirm || 'Yakin ingin menghapus tugas ini?';
        deleteConfirmation.hidden = false;
        confirmDelete.focus();
    });
});

cancelDelete.addEventListener('click', () => {
    closeDeleteConfirmation();
});
confirmDelete.addEventListener('click', () => {
    if (!pendingDeleteForm) {
        return;
    }

    const form = pendingDeleteForm;
    pendingDeleteForm = null;
    confirmedDeleteForm = form;
    deleteConfirmation.hidden = true;
    form.requestSubmit();
});

document.querySelectorAll('.alert').forEach((alert) => {
    alert.querySelector('.alert-close').addEventListener('click', () => alert.remove());
    window.setTimeout(() => alert.remove(), 6000);
});
updateSelection();
