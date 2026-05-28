// static/js/sidebar.js
// Handles mobile sidebar open/close behavior.
// The sidebar is hidden on small screens and slides in when toggled.

/**
 * Toggle the mobile sidebar.
 * Called by the hamburger button in navbar.html.
 *
 * How it works:
 * - The sidebar starts with class '-translate-x-full' (hidden off-screen left)
 * - We remove that class to slide it in
 * - We show a dark overlay behind it
 * - Clicking the overlay or close button slides it back out
 */
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');

  if (!sidebar || !overlay) return;

  // Check if sidebar is currently hidden
  const isHidden = sidebar.classList.contains('-translate-x-full');

  if (isHidden) {
    // OPEN: slide sidebar in from left
    sidebar.classList.remove('-translate-x-full');
    overlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden'; // prevent background scroll
  } else {
    // CLOSE: slide sidebar back out
    closeSidebar();
  }
}

/**
 * Close the sidebar.
 * Called when overlay is clicked or window is resized to desktop.
 */
function closeSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');

  if (sidebar) sidebar.classList.add('-translate-x-full');
  if (overlay) overlay.classList.add('hidden');
  document.body.style.overflow = ''; // restore scrolling
}

// Auto-close sidebar when screen becomes desktop width
window.addEventListener('resize', function () {
  if (window.innerWidth >= 1024) {
    closeSidebar();
  }
});

// Close sidebar when pressing Escape key
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closeSidebar();
});
