// static/js/dashboard.js
// Main dashboard JavaScript controller.
// Handles all AJAX actions using the Fetch API.
//
// What is Fetch API?
// fetch() is a built-in browser function that sends HTTP requests
// from JavaScript — without reloading the page.
// It returns a Promise (an async result that comes back later).

// ---------------------------------------------------------------
// PRAYER ACTIONS
// ---------------------------------------------------------------

/**
 * Approve a prayer request via AJAX.
 * Sends POST to /dashboard/prayers/<id>/approve
 * Updates the UI without a page reload.
 *
 * @param {number} prayerId  - The prayer request ID
 * @param {HTMLElement} btn  - The button that was clicked
 */
async function approvePrayer(prayerId, btn) {
  // Show modal to confirm first
  showModal({
    title:       'Approve Prayer',
    message:     'Mark this prayer request as approved?',
    confirmText: 'Yes, Approve',
    type:        'warning',
    onConfirm:   () => _sendPrayerAction(prayerId, 'approve', btn)
  });
}

async function answerPrayer(prayerId, btn) {
  showModal({
    title:       'Mark as Answered',
    message:     'Mark this prayer as answered? 🙏',
    confirmText: 'Yes, Answered',
    type:        'warning',
    onConfirm:   () => _sendPrayerAction(prayerId, 'answer', btn)
  });
}

async function deletePrayer(prayerId, btn) {
  showModal({
    title:       'Delete Prayer',
    message:     'Are you sure? This cannot be undone.',
    confirmText: 'Yes, Delete',
    type:        'danger',
    onConfirm:   () => _deletePrayerRequest(prayerId, btn)
  });
}

/**
 * Internal function — sends the approve/answer action to Flask.
 *
 * async/await explained:
 * - async means this function runs asynchronously (won't freeze the page)
 * - await means "wait for this promise to finish before continuing"
 * - Without await, the code would continue before the fetch is done
 */
async function _sendPrayerAction(prayerId, action, btn) {
  // Disable button to prevent double-clicking
  setButtonLoading(btn, true);

  try {
    // fetch() sends an HTTP request
    // We send POST to /dashboard/prayers/<id>/approve or /answer
    const response = await fetch(`/dashboard/prayers/${prayerId}/${action}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Send the CSRF token for security (see Step 10)
        'X-CSRFToken': getCSRFToken()
      }
    });

    // response.json() reads the JSON body of the response
    const data = await response.json();

    if (response.ok && data.status === 'success') {
      toastSuccess(data.message || 'Prayer updated!');

      // Find the row in the table and update it
      const row = btn.closest('tr');
      if (row) updatePrayerRow(row, action);

    } else {
      toastError(data.message || 'Something went wrong.');
    }

  } catch (error) {
    // catch() runs if the network request itself failed
    // (e.g. server is down, no internet)
    toastError('Network error. Please try again.');
    console.error('Prayer action error:', error);

  } finally {
    // finally always runs — re-enable button
    setButtonLoading(btn, false);
  }
}

async function _deletePrayerRequest(prayerId, btn) {
  setButtonLoading(btn, true);

  try {
    const response = await fetch(`/dashboard/prayers/${prayerId}/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      }
    });

    const data = await response.json();

    if (response.ok && data.status === 'success') {
      toastSuccess('Prayer request deleted.');

      // Remove the row from the table smoothly
      const row = btn.closest('tr');
      if (row) {
        row.style.transition = 'opacity 0.3s ease';
        row.style.opacity    = '0';
        setTimeout(() => row.remove(), 300);
      }

    } else {
      toastError(data.message || 'Could not delete.');
    }

  } catch (error) {
    toastError('Network error. Please try again.');
  } finally {
    setButtonLoading(btn, false);
  }
}


// ---------------------------------------------------------------
// USER ACTIONS
// ---------------------------------------------------------------

async function promoteUser(userId, username, btn) {
  showModal({
    title:       'Promote to Admin',
    message:     `Give admin access to ${username}?`,
    confirmText: 'Yes, Promote',
    type:        'warning',
    onConfirm:   () => _sendUserAction(userId, 'promote', btn)
  });
}

async function deleteUser(userId, username, btn) {
  showModal({
    title:       'Delete User',
    message:     `Delete ${username}? All their data will be removed.`,
    confirmText: 'Yes, Delete',
    type:        'danger',
    onConfirm:   () => _sendUserAction(userId, 'delete', btn)
  });
}

async function _sendUserAction(userId, action, btn) {
  setButtonLoading(btn, true);

  const method = action === 'delete' ? 'DELETE' : 'POST';
  const url    = action === 'delete'
    ? `/dashboard/users/${userId}/delete`
    : `/dashboard/users/${userId}/promote`;

  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      }
    });

    const data = await response.json();

    if (response.ok && data.status === 'success') {
      toastSuccess(data.message || 'Done!');

      if (action === 'delete') {
        const row = btn.closest('tr');
        if (row) {
          row.style.transition = 'opacity 0.3s ease';
          row.style.opacity    = '0';
          setTimeout(() => row.remove(), 300);
        }
      } else {
        // Reload page to reflect new role badge
        setTimeout(() => location.reload(), 1000);
      }

    } else {
      toastError(data.message || 'Action failed.');
    }

  } catch (error) {
    toastError('Network error. Please try again.');
  } finally {
    setButtonLoading(btn, false);
  }
}


// ---------------------------------------------------------------
// DASHBOARD STATS REFRESH
// ---------------------------------------------------------------

/**
 * Fetch fresh stats from the API and update the dashboard cards.
 * Called automatically every 30 seconds on the dashboard page.
 */
async function refreshDashboardStats() {
  try {
    const response = await fetch('/dashboard/stats', {
      headers: { 'X-CSRFToken': getCSRFToken() }
    });

    if (!response.ok) return;

    const data = await response.json();
    const stats = data.data;

    // Update each stat card by its data-stat attribute
    // e.g. <p data-stat="total_users">0</p>
    updateStatCard('total_users',    stats.total_users);
    updateStatCard('total_prayers',  stats.total_prayers);
    updateStatCard('total_visitors', stats.total_visitors);
    updateStatCard('pending_prayers', stats.pending_prayers);
    updateStatCard('approved_prayers', stats.approved_prayers);
    updateStatCard('answered_prayers', stats.answered_prayers);

  } catch (error) {
    // Silent fail — don't show error for background refresh
    console.warn('Stats refresh failed:', error);
  }
}

function updateStatCard(statName, newValue) {
  const el = document.querySelector(`[data-stat="${statName}"]`);
  if (el && el.textContent !== String(newValue)) {
    el.textContent = newValue;
    // Brief highlight animation
    el.classList.add('text-blue-600');
    setTimeout(() => el.classList.remove('text-blue-600'), 1000);
  }
}


// ---------------------------------------------------------------
// UTILITY FUNCTIONS
// ---------------------------------------------------------------

/**
 * Set a button into a loading/disabled state.
 * Prevents double-clicking and shows feedback.
 *
 * @param {HTMLElement} btn     - The button element
 * @param {boolean} isLoading  - True to disable, false to re-enable
 */
function setButtonLoading(btn, isLoading) {
  if (!btn) return;

  if (isLoading) {
    btn.disabled              = true;
    btn.dataset.originalText  = btn.textContent;
    btn.textContent           = '...';
    btn.classList.add('opacity-60', 'cursor-not-allowed');
  } else {
    btn.disabled     = false;
    btn.textContent  = btn.dataset.originalText || btn.textContent;
    btn.classList.remove('opacity-60', 'cursor-not-allowed');
  }
}

/**
 * Get the CSRF token from the meta tag in base.html.
 * Sent with every fetch request for security.
 */
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.content : '';
}

/**
 * Update a prayer row's status badge after an action.
 */
function updatePrayerRow(row, action) {
  const statusCell = row.querySelector('[data-status-badge]');
  if (!statusCell) return;

  const newStatus = action === 'approve' ? 'approved' : 'answered';
  const colors = {
    approved: 'bg-blue-100 text-blue-700',
    answered: 'bg-green-100 text-green-700'
  };

  statusCell.textContent = newStatus;
  statusCell.className   = `px-2.5 py-1 rounded-full text-xs font-medium ${colors[newStatus]}`;

  // Hide the approve button after approving
  const approveBtn = row.querySelector('[data-action="approve"]');
  if (approveBtn) approveBtn.closest('form, div')?.remove();
}


// ---------------------------------------------------------------
// INIT — runs when page loads
// ---------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {

  // Auto-refresh stats every 30 seconds on dashboard page
  // document.getElementById('stat-cards') is only on the main dashboard
  if (document.getElementById('stat-cards')) {
    setInterval(refreshDashboardStats, 30000);
  }

});
