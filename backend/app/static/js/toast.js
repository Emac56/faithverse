// static/js/toast.js
// Reusable toast notification system.
// Shows a small popup message at the top-right of the screen.
// Auto-hides after 3 seconds.

/**
 * Show a toast notification.
 *
 * @param {string} message - The text to display
 * @param {string} type    - 'success', 'error', 'warning', or 'info'
 * @param {number} duration - How long to show (ms), default 3000
 *
 * Usage:
 *   showToast('Prayer approved!', 'success');
 *   showToast('Something went wrong.', 'error');
 */
function showToast(message, type = 'info', duration = 3000) {

  // Create the toast container if it doesn't exist yet
  // We attach all toasts to this one container
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';

    // Position: top-right corner, on top of everything (z-50)
    container.className = 'fixed top-4 right-4 z-50 flex flex-col gap-2';
    document.body.appendChild(container);
  }

  // Color classes based on type
  const styles = {
    success: 'bg-green-500 text-white',
    error:   'bg-red-500 text-white',
    warning: 'bg-yellow-500 text-white',
    info:    'bg-blue-500 text-white'
  };

  // Icon based on type
  const icons = {
    success: '✅',
    error:   '❌',
    warning: '⚠️',
    info:    'ℹ️'
  };

  // Create the toast element
  const toast = document.createElement('div');
  toast.className = `
    flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg text-sm
    font-medium min-w-64 max-w-sm
    transform translate-x-0 transition-all duration-300
    ${styles[type] || styles.info}
  `;

  toast.innerHTML = `
    <span class="flex-shrink-0">${icons[type] || icons.info}</span>
    <span class="flex-1">${message}</span>
    <button onclick="this.parentElement.remove()"
            class="flex-shrink-0 ml-2 opacity-70 hover:opacity-100 text-lg leading-none">
      ×
    </button>
  `;

  // Add to container
  container.appendChild(toast);

  // Auto-remove after duration
  // setTimeout runs a function after a delay (in milliseconds)
  setTimeout(() => {
    // Fade out animation
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';

    // Remove from DOM after animation completes
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

/**
 * Shortcut functions for common toast types.
 * Instead of showToast('msg', 'success') you can write toastSuccess('msg')
 */
const toastSuccess = (msg) => showToast(msg, 'success');
const toastError   = (msg) => showToast(msg, 'error');
const toastWarning = (msg) => showToast(msg, 'warning');
const toastInfo    = (msg) => showToast(msg, 'info');
