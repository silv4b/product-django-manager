function openDeleteAccountModal() {
    const modal = document.getElementById('deleteAccountModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeDeleteAccountModal() {
    const modal = document.getElementById('deleteAccountModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
    
    // Reset inputs for security and usability
    const confirmUsername = document.getElementById('confirm_username');
    if (confirmUsername) confirmUsername.value = '';

    const confirmPassword = document.getElementById('confirm_password');
    if (confirmPassword) confirmPassword.value = '';
    
    // This function is defined inline in the HTML because it has Django dependencies.
    // We try to call it to reset the button state.
    if (typeof validateDeletion === 'function') {
        validateDeletion();
    }
}

function copyPublicLink() {
    const input = document.getElementById('public-link-input');
    const icon = document.getElementById('copy-icon');
    if (!input || !icon) return;

    input.select();
    input.setSelectionRange(0, 99999); // For mobile devices
    
    navigator.clipboard.writeText(input.value).then(() => {
        // Use a more robust way to handle icon switching
        const originalIconName = 'copy';
        const successIconName = 'check';

        icon.setAttribute('data-lucide', successIconName);
        icon.classList.add('text-green-500');
        lucide.createIcons();

        setTimeout(() => {
            icon.setAttribute('data-lucide', originalIconName);
            icon.classList.remove('text-green-500');
            lucide.createIcons();
        }, 2000);
    }).catch(err => {
        console.error('Could not copy text: ', err);
        // Optionally provide user feedback on failure
    });
}
