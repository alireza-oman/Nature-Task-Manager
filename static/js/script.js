// 🌙 مدیریت حالت تاریک و ذخیره در LocalStorage
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeIcon();
}

function updateThemeIcon() {
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
        themeBtn.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    }
}

// بارگذاری اولیه تم
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }
    updateThemeIcon();
});

// باز کردن مودال ویرایش سریع
function openEditModal(taskId, currentTitle, currentPriority, currentCategory) {
    document.getElementById('modal-task-id').value = taskId;
    document.getElementById('modal-title').value = currentTitle;
    document.getElementById('modal-priority').value = currentPriority;
    document.getElementById('modal-category').value = currentCategory || 'personal';
    document.getElementById('full-edit-link').href = `/full_edit/${taskId}`;
    document.getElementById('editModal').classList.add('show');
}

function closeModal() {
    document.getElementById('editModal').classList.remove('show');
}

window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target === modal) {
        closeModal();
    }
}