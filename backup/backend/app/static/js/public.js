// static/js/public.js
// JavaScript for the FaithVerse public website.
// Phase 7.2: Enhanced mobile navigation.

// ---------------------------------------------------------------
// MOBILE NAVIGATION TOGGLE
// ---------------------------------------------------------------

/**
 * toggleMobileMenu()
 *
 * Called by the hamburger button: onclick="toggleMobileMenu()"
 *
 * What it does:
 * 1. Toggles 'open' class on #mobile-menu  → CSS shows/hides it
 * 2. Updates aria-expanded on the button   → accessibility
 * 3. Updates aria-hidden on the menu       → accessibility
 * 4. Locks body scroll while menu is open  → prevents background scroll on mobile
 */
function toggleMobileMenu() {
  const menu      = document.getElementById('mobile-menu');
  const hamburger = document.getElementById('nav-hamburger');

  if (!menu || !hamburger) return;

  const isOpen = menu.classList.toggle('open');

  // Update ARIA attributes for screen readers
  hamburger.setAttribute('aria-expanded', isOpen);
  menu.setAttribute('aria-hidden', !isOpen);

  // Lock body scroll when menu is open (prevents scrolling behind the menu)
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

/**
 * Close mobile menu when any link inside it is clicked.
 * Gives smooth UX — tap a link, menu closes, page loads.
 */
function closeMobileMenuOnNavClick() {
  const menu  = document.getElementById('mobile-menu');
  const links = document.querySelectorAll('.mobile-menu a');

  links.forEach(link => {
    link.addEventListener('click', () => {
      if (menu) {
        menu.classList.remove('open');
        document.body.style.overflow = '';

        const hamburger = document.getElementById('nav-hamburger');
        if (hamburger) {
          hamburger.setAttribute('aria-expanded', 'false');
        }
        menu.setAttribute('aria-hidden', 'true');
      }
    });
  });
}

/**
 * Close mobile menu when ESC key is pressed.
 * Standard keyboard accessibility behavior.
 */
function closeMobileMenuOnEsc() {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const menu = document.getElementById('mobile-menu');
      if (menu && menu.classList.contains('open')) {
        toggleMobileMenu();
      }
    }
  });
}

// ---------------------------------------------------------------
// SERVER-SIDE ACTIVE LINK (backup)
// The navbar partial uses Jinja2 server-side detection.
// This JS runs client-side as a fallback for edge cases.
// ---------------------------------------------------------------

function setActiveNavLink() {
  const currentPath = window.location.pathname;
  const navLinks    = document.querySelectorAll('.nav-links a, .mobile-menu a');

  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;

    // Strip query strings and hashes for comparison
    const cleanHref = href.split('?')[0].split('#')[0];

    if (cleanHref === '/' && currentPath === '/') {
      link.classList.add('active');
    } else if (cleanHref !== '/' && currentPath.startsWith(cleanHref)) {
      link.classList.add('active');
    }
  });
}

// ---------------------------------------------------------------
// FLASH MESSAGE AUTO-DISMISS
// ---------------------------------------------------------------

/**
 * Flash messages auto-dismiss after 5 seconds.
 * Clicking a message dismisses it immediately.
 */
function initFlashMessages() {
  const alerts = document.querySelectorAll('.flash-alert');

  alerts.forEach(alert => {
    // Auto-dismiss after 5s
    const timer = setTimeout(() => {
      dismissAlert(alert);
    }, 5000);

    // Click to dismiss early
    alert.addEventListener('click', () => {
      clearTimeout(timer);
      dismissAlert(alert);
    });
  });
}

function dismissAlert(alert) {
  alert.style.opacity    = '0';
  alert.style.transform  = 'translateX(120%)';
  alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  setTimeout(() => alert.remove(), 400);
}

// ---------------------------------------------------------------
// SMOOTH SCROLL FOR ANCHOR LINKS
// Handles: href="#submit" on the Prayer Wall page
// ---------------------------------------------------------------

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href').slice(1);
      const target   = document.getElementById(targetId);

      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

// ---------------------------------------------------------------
// NAVBAR SCROLL EFFECT
// Adds a subtle shadow to the navbar when the page is scrolled.
// ---------------------------------------------------------------

function initNavbarScrollEffect() {
  const nav = document.querySelector('.public-nav');
  if (!nav) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      nav.style.boxShadow = '0 2px 20px rgba(109, 40, 217, 0.12)';
    } else {
      nav.style.boxShadow = 'none';
    }
  }, { passive: true });
}

// ---------------------------------------------------------------
// INITIALISE — Runs when HTML is fully loaded
// ---------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
  closeMobileMenuOnNavClick();
  closeMobileMenuOnEsc();
  setActiveNavLink();
  initFlashMessages();
  initSmoothScroll();
  initNavbarScrollEffect();
});
