// static/js/modal.js
// Reusable confirmation modal system.
// Shows a popup asking "Are you sure?" before dangerous actions.

/**
 * Show a confirmation modal.
 *
 * @param {object} options - Configuration object
 * @param {string} options.title      - Modal title
 * @param {string} options.message    - Warning message
 * @param {string} options.confirmText - Text for confirm button (default: 'Confirm')
 * @param {string} options.type       - 'danger' or 'warning' (affects button color)
 * @param {function} options.onConfirm - Function to run when confirmed
 *
 * Usage:
 *   showModal({
 *     title: 'Delete User',
 *     message: 'Are you sure you want to delete john_doe?',
 *     confirmText: 'Yes, Delete',
 *     type: 'danger',
 *     onConfirm: () => deleteUser(5)
 *   });
 */
function showModal({ title, message, confirmText = 'Confirm', type = 'danger', onConfirm }) {

  // Remove any existing modal first
  const existing = document.getElementById('confirm-modal');
  if (existing) existing.remove();

  // Button color based on type
  const btnColor = type === 'danger'
    ? 'bg-red-600 hover:bg-red-700 text-white'
    : 'bg-yellow-500 hover:bg-yellow-600 text-white';

  // Build modal HTML
  const modal = document.createElement('div');
  modal.id = 'confirm-modal';

  // Full screen overlay
  modal.className = 'fixed inset-0 z-50 flex items-center justify-center px-4';
  modal.innerHTML = `

    <!-- Dark background overlay -->
    <div class="absolute inset-0 bg-black bg-opacity-50"
         onclick="closeModal()"></div>

    <!-- Modal box -->
    <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 z-10">

      <!-- Icon -->
      <div class="text-center mb-4">
        <span class="text-5xl">${type === 'danger' ? '🗑️' : '⚠️'}</span>
      </div>

      <!-- Title -->
      <h3 class="text-lg font-bold text-gray-800 text-center mb-2">
        ${title}
      </h3>

      <!-- Message -->
      <p class="text-sm text-gray-500 text-center mb-6">
        ${message}
      </p>

      <!-- Buttons -->
      <div class="flex gap-3">

        <!-- Cancel button -->
        <button onclick="closeModal()"
                class="flex-1 px-4 py-2.5 rounded-lg text-sm font-medium
                       border border-gray-200 text-gray-600
                       hover:bg-gray-50 transition">
          Cancel
        </button>

        <!-- Confirm button -->
        <button id="modal-confirm-btn"
                class="flex-1 px-4 py-2.5 rounded-lg text-sm font-medium
                       transition ${btnColor}">
          ${confirmText}
        </button>

      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // Attach the confirm action
  // We use a separate assignment to avoid inline onclick with complex functions
  document.getElementById('modal-confirm-btn').addEventListener('click', function () {
    closeModal();
    if (typeof onConfirm === 'function') onConfirm();
  });

  // Close on Escape key
  document.addEventListener('keydown', handleModalEscape);
}

/**
 * Close and remove the confirmation modal.
 */
function closeModal() {
  const modal = document.getElementById('confirm-modal');
  if (modal) modal.remove();
  document.removeEventListener('keydown', handleModalEscape);
}

function handleModalEscape(e) {
  if (e.key === 'Escape') closeModal();
}
