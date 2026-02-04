function closeToast(button) {
    const toast = button.closest('.toast');
    if (!toast) return;
    toast.classList.add('animate-out', 'fade-out', 'slide-out-to-right-full', 'duration-500');
    setTimeout(() => toast.remove(), 500);
}

function toggleLogoutModal(show) {
    const modal = document.getElementById('logoutModal');
    if (!modal) return;
    if (show) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

function togglePasswordVisibility(button) {
    const input = button.parentElement.querySelector('input');
    const iconEye = button.querySelector('[data-lucide="eye"]');
    const iconEyeOff = button.querySelector('[data-lucide="eye-off"]');

    if (!input || !iconEye || !iconEyeOff) return;

    if (input.type === 'password') {
        input.type = 'text';
        iconEye.classList.add('hidden');
        iconEyeOff.classList.remove('hidden');
    } else {
        input.type = 'password';
        iconEye.classList.remove('hidden');
        iconEyeOff.classList.add('hidden');
    }
}

function closeModal() {
    const modalContainer = document.getElementById('modal-container');
    if (modalContainer) {
        modalContainer.innerHTML = '';
    }
}

// --- Initializers ---

// Initialize global scripts on first page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize lucide icons
    lucide.createIcons();

    // Auto-hide existing toasts that are present on page load
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            // Check if toast is still in the DOM
            if (toast.parentElement) {
                toast.classList.add('animate-out', 'fade-out', 'slide-out-to-right-full', 'duration-500');
                setTimeout(() => toast.remove(), 500);
            }
        }, 6000);
    });
});


// Add HTMX integration for re-initializing icons after AJAX content swaps
document.body.addEventListener('htmx:afterSwap', function (evt) {
    // When a modal or other dynamic content is loaded, re-run lucide to render new icons
    lucide.createIcons();
});

// Add global keyboard shortcut for closing modals via Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});
