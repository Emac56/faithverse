/**
 * FaithVerse — app.js
 * Phase 3: Hero parallax, bookmark/favorites, mobile layout improvements,
 * back-to-top button, bookmarks panel (bottom sheet on mobile).
 */

import { supabase } from './supabase.js';

gsap.registerPlugin(ScrollTrigger, TextPlugin);

// ─────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────
const STORAGE_KEY_DARK      = "faithverse-dark";
const STORAGE_KEY_BOOKMARKS = "faithverse-bookmarks";

const VERSE_REFS = [
  "philippians 4:13", "jeremiah 29:11", "psalm 23:1",     "joshua 1:9",
  "proverbs 3:5",     "psalm 46:10",    "psalm 34:18",    "matthew 11:28",
  "romans 8:28",      "isaiah 40:31",   "philippians 4:6","psalm 46:1",
  "isaiah 41:10",     "matthew 6:33",   "ephesians 3:20", "hebrews 11:1",
  "romans 15:13",     "exodus 14:14",   "1 peter 5:7",    "psalm 139:14",
  "matthew 19:26",    "nehemiah 8:10",  "psalm 147:3",    "romans 8:31",
  "psalm 119:105",    "psalm 107:1",    "psalm 37:4",     "galatians 6:9",
  "2 corinthians 12:9","john 16:33",    "psalm 27:1",     "proverbs 31:25",
  "zephaniah 3:17",   "psalm 91:11",    "romans 5:8",     "john 14:27",
];

// ─────────────────────────────────────────────
// DOM REFERENCES
// ─────────────────────────────────────────────
const dom = {
  darkToggle:           document.getElementById("dark-toggle"),
  darkIcon:             document.getElementById("dark-icon"),
  darkToggleSidebar:    document.getElementById("dark-toggle-sidebar"),
  darkIconSidebar:      document.getElementById("dark-icon-sidebar"),
  menuBtn:              document.getElementById("menu-btn"),
  sidebar:              document.getElementById("sidebar"),
  sidebarOverlay:       document.getElementById("sidebar-overlay"),
  sidebarClose:         document.getElementById("sidebar-close"),
  currentDate:          document.getElementById("current-date"),
  verseContent:         document.getElementById("verse-content"),
  verseText:            document.getElementById("verse-text"),
  verseReference:       document.getElementById("verse-reference"),
  newVerseBtn:          document.getElementById("new-verse-btn"),
  copyBtn:              document.getElementById("copy-btn"),
  shareBtn:             document.getElementById("share-btn"),
  bookmarkBtn:          document.getElementById("bookmark-btn"),
  bookmarkIcon:         document.getElementById("bookmark-icon"),
  bookmarkBtnLabel:     document.getElementById("bookmark-btn-label"),
  prayerForm:           document.getElementById("prayer-form"),
  formName:             document.getElementById("form-name"),
  formMessage:          document.getElementById("form-message"),
  submitBtn:            document.getElementById("submit-btn"),
  scrollProgress:       document.getElementById("scroll-progress"),
  toastContainer:       document.getElementById("toast-container"),
  heroBg:               document.getElementById("hero-bg"),
  backToTop:            document.getElementById("back-to-top"),
  // Bookmarks modal
  bookmarksModal:       document.getElementById("bookmarks-modal"),
  bookmarksOverlay:     document.getElementById("bookmarks-overlay"),
  bookmarksPanel:       document.getElementById("bookmarks-panel"),
  bookmarksClose:       document.getElementById("bookmarks-close"),
  bookmarksList:        document.getElementById("bookmarks-list"),
  bookmarksCount:       document.getElementById("bookmarks-count"),
  clearBookmarksBtn:    document.getElementById("clear-bookmarks-btn"),
  bookmarksToggleBtn:   document.getElementById("bookmarks-toggle-btn"),
  bookmarksToggleSidebar: document.getElementById("bookmarks-toggle-sidebar"),
  bookmarkNavBadge:     document.getElementById("bookmark-nav-badge"),
  bookmarkSidebarBadge: document.getElementById("bookmark-sidebar-badge"),
};

// ─────────────────────────────────────────────
// 1. TOAST
// ─────────────────────────────────────────────
function showToast(message, icon = "fa-circle-check", isError = false) {
  const toast = document.createElement("div");
  toast.className = `toast${isError ? " error" : ""}`;
  toast.setAttribute("role", "status");
  toast.innerHTML = `<i class="fa-solid ${icon}" aria-hidden="true"></i><span>${message}</span>`;
  dom.toastContainer.appendChild(toast);
  requestAnimationFrame(() => requestAnimationFrame(() => toast.classList.add("show")));
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 350);
  }, 2800);
}

// ─────────────────────────────────────────────
// 2. DATE
// ─────────────────────────────────────────────
function initDate() {
  if (!dom.currentDate) return;
  const today = new Date();
  dom.currentDate.textContent = today.toLocaleDateString("en-US", {
    year: "numeric", month: "long", day: "numeric",
  });
  dom.currentDate.setAttribute("datetime", today.toISOString().slice(0, 10));
}

// ─────────────────────────────────────────────
// 3. DARK MODE
// ─────────────────────────────────────────────
function applyDark(isDark) {
  document.documentElement.classList.toggle("dark", isDark);
  localStorage.setItem(STORAGE_KEY_DARK, isDark ? "1" : "0");
  const icon  = isDark ? "fa-solid fa-sun"  : "fa-solid fa-moon";
  const label = isDark ? "Switch to light mode" : "Switch to dark mode";
  if (dom.darkIcon)          dom.darkIcon.className = icon;
  if (dom.darkIconSidebar)   dom.darkIconSidebar.className = icon;
  if (dom.darkToggle)        dom.darkToggle.setAttribute("aria-label", label);
  if (dom.darkToggleSidebar) dom.darkToggleSidebar.setAttribute("aria-label", label);
}

function toggleDark() {
  const isDark = !document.documentElement.classList.contains("dark");
  applyDark(isDark);
  showToast(isDark ? "Dark mode on" : "Light mode on", isDark ? "fa-moon" : "fa-sun");
}

function initDarkMode() {
  applyDark(localStorage.getItem(STORAGE_KEY_DARK) === "1");
  dom.darkToggle?.addEventListener("click", toggleDark);
  dom.darkToggleSidebar?.addEventListener("click", toggleDark);
}

// ─────────────────────────────────────────────
// 4. SCROLL PROGRESS + BACK TO TOP
// ─────────────────────────────────────────────
function initScrollProgress() {
  if (!dom.scrollProgress) return;
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const scrolled = window.scrollY;
      const total    = document.documentElement.scrollHeight - window.innerHeight;
      dom.scrollProgress.style.width = total > 0 ? `${(scrolled / total) * 100}%` : "0%";

      // Back to top visibility
      if (dom.backToTop) {
        if (scrolled > 400) {
          dom.backToTop.classList.add("visible");
        } else {
          dom.backToTop.classList.remove("visible");
        }
      }

      ticking = false;
    });
  }, { passive: true });

  dom.backToTop?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

// ─────────────────────────────────────────────
// 5. SIDEBAR
// ─────────────────────────────────────────────
let sidebarOpen = false;

function openSidebar() {
  if (sidebarOpen) return;
  sidebarOpen = true;
  dom.sidebarOverlay.classList.remove("hidden");
  dom.sidebarOverlay.removeAttribute("aria-hidden");
  dom.menuBtn.setAttribute("aria-expanded", "true");
  document.body.style.overflow = "hidden";
  gsap.fromTo(dom.sidebar,        { x: "100%" }, { x: "0%", duration: 0.35, ease: "power3.out" });
  gsap.fromTo(dom.sidebarOverlay, { opacity: 0 }, { opacity: 1, duration: 0.3 });
  dom.sidebarClose?.focus();
}

function closeSidebar() {
  if (!sidebarOpen) return;
  sidebarOpen = false;
  dom.menuBtn.setAttribute("aria-expanded", "false");
  document.body.style.overflow = "";
  gsap.to(dom.sidebar, { x: "100%", duration: 0.3, ease: "power3.in" });
  gsap.to(dom.sidebarOverlay, {
    opacity: 0, duration: 0.3,
    onComplete: () => {
      dom.sidebarOverlay.classList.add("hidden");
      dom.sidebarOverlay.setAttribute("aria-hidden", "true");
    },
  });
  dom.menuBtn?.focus();
}

function initSidebar() {
  dom.menuBtn?.addEventListener("click", openSidebar);
  dom.sidebarClose?.addEventListener("click", closeSidebar);
  dom.sidebarOverlay?.addEventListener("click", closeSidebar);
  document.querySelectorAll(".sidebar-link").forEach(l => l.addEventListener("click", closeSidebar));
  document.addEventListener("keydown", e => { if (e.key === "Escape" && sidebarOpen) closeSidebar(); });
}

// ─────────────────────────────────────────────
// 6. ACTIVE NAV
// ─────────────────────────────────────────────
function initActiveNav() {
  const sections     = document.querySelectorAll("section[id]");
  const navLinks     = document.querySelectorAll(".nav-link");
  const sidebarLinks = document.querySelectorAll(".sidebar-link");

  function setActive(id) {
    navLinks.forEach(a     => a.classList.toggle("active", a.dataset.section === id));
    sidebarLinks.forEach(a => a.classList.toggle("active", a.dataset.section === id));
  }

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) setActive(e.target.id); });
  }, { threshold: 0.25, rootMargin: "-60px 0px -35% 0px" });

  sections.forEach(s => obs.observe(s));
}

// ─────────────────────────────────────────────
// 7. HERO PARALLAX (Phase 3)
// ─────────────────────────────────────────────
function initHeroParallax() {
  if (!dom.heroBg) return;

  // Use ScrollTrigger for smooth parallax
  const heroSection = document.getElementById("hero-section") || document.getElementById("home");
  if (!heroSection) return;

  gsap.to(dom.heroBg, {
    yPercent: 25,           // move down 25% of image height as user scrolls through hero
    ease: "none",
    scrollTrigger: {
      trigger: heroSection,
      start: "top top",
      end: "bottom top",
      scrub: 0.6,           // smooth lag
    },
  });
}

// ─────────────────────────────────────────────
// 8. ANIMATIONS — scroll reveals + hover lifts
// ─────────────────────────────────────────────
function initAnimations() {

  // Scroll reveals
  gsap.utils.toArray(".card-scroll").forEach(el => {
    gsap.from(el, {
      y: 50, opacity: 0, duration: 0.6, ease: "power3.out",
      scrollTrigger: { trigger: el, start: "top 92%", toggleActions: "play none none reverse" },
    });
  });

  gsap.from(".date-badge", {
    y: -20, opacity: 0, duration: 0.8, ease: "power3.out",
    scrollTrigger: { trigger: ".date-badge", start: "top 90%" },
  });

  // Devotion cards staggered directional reveal
  gsap.utils.toArray(".devotion-card").forEach(card => {
    const icon  = card.querySelector(".devotion-icon");
    const title = card.querySelector(".devotion-title");
    const text  = card.querySelector(".devotion-text");
    const st    = { trigger: card, start: "top 88%", toggleActions: "play none none reverse" };
    gsap.from(icon,  { x: -30, opacity: 0, duration: 0.5, scrollTrigger: st });
    gsap.from(title, { y: -15, opacity: 0, duration: 0.5, delay: 0.12, scrollTrigger: st });
    gsap.from(text,  { x: 30,  opacity: 0, duration: 0.5, delay: 0.24, scrollTrigger: st });
  });

  // Button micro-interactions
  document.querySelectorAll("#new-verse-btn, #share-btn, #copy-btn, #bookmark-btn").forEach(btn => {
    btn.addEventListener("mouseenter", () => gsap.to(btn, { scale: 1.04, duration: 0.15 }));
    btn.addEventListener("mouseleave", () => gsap.to(btn, { scale: 1,    duration: 0.15 }));
  });

  // Devotion card hover lift
  document.querySelectorAll(".devotion-card").forEach(card => {
    card.addEventListener("mouseenter", () =>
      gsap.to(card, { y: -6, scale: 1.03, duration: 0.3, ease: "power2.out" })
    );
    card.addEventListener("mouseleave", () =>
      gsap.to(card, { y: 0, scale: 1, duration: 0.3, ease: "power2.out" })
    );
  });

  // Prayer card hover lift
  document.querySelectorAll(".prayer-card").forEach(card => {
    card.addEventListener("mouseenter", () =>
      gsap.to(card, { y: -5, scale: 1.02, duration: 0.3, ease: "power2.out" })
    );
    card.addEventListener("mouseleave", () =>
      gsap.to(card, { y: 0, scale: 1, duration: 0.3, ease: "power2.out" })
    );
  });

  // About & Contact hover lift
  document.querySelectorAll("#about, #contact").forEach(section => {
    section.addEventListener("mouseenter", () =>
      gsap.to(section, { y: -4, scale: 1.01, duration: 0.3, ease: "power2.out" })
    );
    section.addEventListener("mouseleave", () =>
      gsap.to(section, { y: 0, scale: 1, duration: 0.3, ease: "power2.out" })
    );
  });
}

// ─────────────────────────────────────────────
// 9. VERSE HELPERS
// ─────────────────────────────────────────────
function getCurrentVerse() {
  return {
    text: dom.verseText?.textContent.trim()      || "",
    ref:  dom.verseReference?.textContent.trim() || "",
  };
}

function setVerseLoading(isLoading) {
  if (!dom.verseContent) return;
  dom.verseContent.classList.toggle("loading", isLoading);
}

function animateVerseIn(text, ref) {
  gsap.to([dom.verseText, dom.verseReference], {
    opacity: 0, duration: 0.2,
    onComplete: () => {
      gsap.to(dom.verseText, {
        duration: Math.min(text.length * 0.022, 2.5),
        text, ease: "none", opacity: 1,
        onComplete: () => updateBookmarkBtnUI(),   // update bookmark state after text set
      });
      if (dom.verseReference) {
        dom.verseReference.textContent = ref;
        gsap.to(dom.verseReference, { opacity: 1, duration: 0.5, delay: 0.4 });
      }
    },
  });
}

function setButtonLoading(btn, isLoading) {
  if (!btn) return;
  btn.disabled = isLoading;
  if (isLoading) {
    btn.dataset.html = btn.innerHTML;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin" aria-hidden="true"></i> Loading...`;
  } else {
    btn.innerHTML = btn.dataset.html || btn.innerHTML;
  }
}

// ─────────────────────────────────────────────
// 10. VERSE OF THE DAY
// ─────────────────────────────────────────────
function loadVerseOfDay() {
  setVerseLoading(true);
  const now  = new Date();
  const seed = now.getFullYear() * 10000 + (now.getMonth() + 1) * 100 + now.getDate();
  const idx  = seed % VERSE_REFS.length;

  fetch(`https://bible-api.com/${VERSE_REFS[idx]}`)
    .then(r => { if (!r.ok) throw new Error(); return r.json(); })
    .then(data => {
      setVerseLoading(false);
      if (dom.verseText)      dom.verseText.textContent      = data.text.trim();
      if (dom.verseReference) dom.verseReference.textContent = data.reference;
      gsap.from([dom.verseText, dom.verseReference], { opacity: 0, y: 10, duration: 0.5, stagger: 0.15 });
      updateBookmarkBtnUI();
    })
    .catch(() => {
      setVerseLoading(false);
      updateBookmarkBtnUI();
    });
}

// ─────────────────────────────────────────────
// 11. NEW VERSE BUTTON
// ─────────────────────────────────────────────
let lastVerseIndex = -1;

function initNewVerseButton() {
  if (!dom.newVerseBtn) return;
  dom.newVerseBtn.addEventListener("click", () => {
    gsap.to(dom.newVerseBtn, {
      scale: 0.92, duration: 0.1, ease: "power2.in",
      onComplete: () => gsap.to(dom.newVerseBtn, { scale: 1, duration: 0.22, ease: "back.out(2)" }),
    });

    setButtonLoading(dom.newVerseBtn, true);

    let idx;
    do { idx = Math.floor(Math.random() * VERSE_REFS.length); }
    while (idx === lastVerseIndex);
    lastVerseIndex = idx;

    fetch(`https://bible-api.com/${VERSE_REFS[idx]}`)
      .then(r => { if (!r.ok) throw new Error(); return r.json(); })
      .then(data => {
        setButtonLoading(dom.newVerseBtn, false);
        animateVerseIn(data.text.trim(), data.reference);
      })
      .catch(() => {
        setButtonLoading(dom.newVerseBtn, false);
        showToast("Couldn't load verse. Try again.", "fa-triangle-exclamation", true);
      });
  });
}

// ─────────────────────────────────────────────
// 12. COPY BUTTON
// ─────────────────────────────────────────────
function initCopyButton() {
  dom.copyBtn?.addEventListener("click", () => {
    const { text, ref } = getCurrentVerse();
    navigator.clipboard.writeText(`"${text}" — ${ref}`)
      .then(() => showToast("Verse copied to clipboard!", "fa-copy"))
      .catch(() => showToast("Copy failed. Try again.", "fa-triangle-exclamation", true));
  });
}

// ─────────────────────────────────────────────
// 13. SHARE BUTTON
// ─────────────────────────────────────────────
function initShareButton() {
  dom.shareBtn?.addEventListener("click", async () => {
    const { text, ref } = getCurrentVerse();
    const shareData = {
      title: "FaithVerse — Daily Bible Verse",
      text:  `"${text}" — ${ref}`,
      url:   window.location.href,
    };
    if (navigator.share) {
      try { await navigator.share(shareData); } catch (_) {}
    } else {
      navigator.clipboard.writeText(`${shareData.text}\n${shareData.url}`)
        .then(() => showToast("Link copied to clipboard!", "fa-share-nodes"))
        .catch(() => showToast("Share failed.", "fa-triangle-exclamation", true));
    }
  });
}

// ─────────────────────────────────────────────
// 14. BOOKMARKS (Phase 3)
// ─────────────────────────────────────────────

function loadBookmarks() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY_BOOKMARKS) || "[]");
  } catch { return []; }
}

function saveBookmarksData(arr) {
  localStorage.setItem(STORAGE_KEY_BOOKMARKS, JSON.stringify(arr));
}

function isCurrentVerseBookmarked() {
  const { text, ref } = getCurrentVerse();
  if (!text || !ref) return false;
  return loadBookmarks().some(b => b.ref === ref);
}

function updateBookmarkBtnUI() {
  const saved = isCurrentVerseBookmarked();

  if (dom.bookmarkIcon) {
    dom.bookmarkIcon.className = saved
      ? "fa-solid fa-bookmark"
      : "fa-regular fa-bookmark";
  }
  if (dom.bookmarkBtnLabel) {
    dom.bookmarkBtnLabel.textContent = saved ? "Saved!" : "Save Verse";
  }
  if (dom.bookmarkBtn) {
    if (saved) {
      dom.bookmarkBtn.classList.add("is-saved");
    } else {
      dom.bookmarkBtn.classList.remove("is-saved");
    }
    dom.bookmarkBtn.setAttribute("aria-label",
      saved ? "Remove from saved verses" : "Save this verse");
  }
}

function updateBookmarkBadges() {
  const count = loadBookmarks().length;

  // Nav badge
  if (dom.bookmarkNavBadge) {
    if (count > 0) {
      dom.bookmarkNavBadge.textContent = count > 99 ? "99+" : count;
      dom.bookmarkNavBadge.classList.add("visible");
    } else {
      dom.bookmarkNavBadge.classList.remove("visible");
    }
  }

  // Sidebar badge
  if (dom.bookmarkSidebarBadge) {
    if (count > 0) {
      dom.bookmarkSidebarBadge.textContent = count;
      dom.bookmarkSidebarBadge.classList.remove("hidden");
    } else {
      dom.bookmarkSidebarBadge.classList.add("hidden");
    }
  }

  // Panel count
  if (dom.bookmarksCount) {
    if (count > 0) {
      dom.bookmarksCount.textContent = `${count} saved`;
      dom.bookmarksCount.classList.remove("hidden");
    } else {
      dom.bookmarksCount.classList.add("hidden");
    }
  }

  // Clear button
  if (dom.clearBookmarksBtn) {
    if (count > 0) {
      dom.clearBookmarksBtn.classList.remove("hidden");
    } else {
      dom.clearBookmarksBtn.classList.add("hidden");
    }
  }
}

function toggleBookmark() {
  const { text, ref } = getCurrentVerse();
  if (!text || !ref) return;

  let bookmarks = loadBookmarks();
  const idx = bookmarks.findIndex(b => b.ref === ref);

  // Bounce animation on button
  if (dom.bookmarkBtn) {
    gsap.to(dom.bookmarkBtn, {
      scale: 0.9, duration: 0.1, ease: "power2.in",
      onComplete: () => gsap.to(dom.bookmarkBtn, { scale: 1, duration: 0.25, ease: "back.out(2.5)" }),
    });
  }

  if (idx >= 0) {
    bookmarks.splice(idx, 1);
    showToast("Removed from saved verses.", "fa-bookmark");
  } else {
    bookmarks.unshift({
      text,
      ref,
      savedAt: new Date().toISOString(),
    });
    showToast("Verse saved! 🔖", "fa-bookmark");
  }

  saveBookmarksData(bookmarks);
  updateBookmarkBtnUI();
  updateBookmarkBadges();

  // If panel is open, re-render list
  if (dom.bookmarksModal?.classList.contains("open")) {
    renderBookmarksList();
  }
}

function renderBookmarksList() {
  if (!dom.bookmarksList) return;
  const bookmarks = loadBookmarks();

  if (bookmarks.length === 0) {
    dom.bookmarksList.innerHTML = `
      <div class="flex flex-col items-center justify-center py-12 gap-4 text-center">
        <div class="w-16 h-16 rounded-2xl flex items-center justify-center" style="background: var(--bg-surface);">
          <i class="fa-regular fa-bookmark text-3xl" style="color: var(--text-muted);"></i>
        </div>
        <div>
          <p class="font-semibold text-sm" style="color: var(--text-primary);">No saved verses yet</p>
          <p class="text-xs mt-1" style="color: var(--text-muted);">Tap "Save Verse" to bookmark a verse</p>
        </div>
      </div>
    `;
    return;
  }

  dom.bookmarksList.innerHTML = bookmarks.map((b, i) => {
    const date = b.savedAt
      ? new Date(b.savedAt).toLocaleDateString("en-US", { month: "short", day: "numeric" })
      : "";
    return `
      <div class="bookmark-item" data-index="${i}" role="button" tabindex="0"
        aria-label="Load verse: ${b.ref}" title="Tap to load this verse">
        <button class="bookmark-remove" data-index="${i}" aria-label="Remove ${b.ref} from saved verses" title="Remove">
          <i class="fa-solid fa-xmark text-xs" aria-hidden="true"></i>
        </button>
        <p class="font-verse text-sm leading-snug pr-8" style="color: var(--text-primary);">
          "${b.text.length > 100 ? b.text.slice(0, 100) + '…' : b.text}"
        </p>
        <div class="flex items-center justify-between mt-2">
          <span class="text-xs font-semibold text-violet-500">${b.ref}</span>
          ${date ? `<span class="text-xs" style="color: var(--text-muted);">${date}</span>` : ""}
        </div>
      </div>
    `;
  }).join("");

  // Tap bookmark item → load verse into card
  dom.bookmarksList.querySelectorAll(".bookmark-item").forEach(item => {
    item.addEventListener("click", (e) => {
      if (e.target.closest(".bookmark-remove")) return; // don't trigger if removing
      const idx = parseInt(item.dataset.index);
      const b   = loadBookmarks()[idx];
      if (!b) return;
      closeBookmarksModal();
      setTimeout(() => {
        animateVerseIn(b.text, b.ref);
        window.scrollTo({ top: 0, behavior: "smooth" });
      }, 350);
    });
    item.addEventListener("keydown", e => {
      if (e.key === "Enter" || e.key === " ") item.click();
    });
  });

  // Remove individual bookmark
  dom.bookmarksList.querySelectorAll(".bookmark-remove").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const idx = parseInt(btn.dataset.index);
      let bookmarks = loadBookmarks();
      if (bookmarks[idx]) {
        bookmarks.splice(idx, 1);
        saveBookmarksData(bookmarks);
        updateBookmarkBtnUI();
        updateBookmarkBadges();
        renderBookmarksList();

        // Animate removal
        const item = btn.closest(".bookmark-item");
        if (item) {
          gsap.to(item, {
            opacity: 0, x: 20, duration: 0.25, ease: "power2.in",
            onComplete: () => renderBookmarksList(),
          });
        }
      }
    });
  });
}

let bookmarksPanelOpen = false;

function openBookmarksModal() {
  if (bookmarksPanelOpen) return;
  bookmarksPanelOpen = true;
  document.body.style.overflow = "hidden";
  renderBookmarksList();
  dom.bookmarksModal?.classList.add("open");
  dom.bookmarksClose?.focus();
}

function closeBookmarksModal() {
  if (!bookmarksPanelOpen) return;
  bookmarksPanelOpen = false;
  document.body.style.overflow = "";
  dom.bookmarksModal?.classList.remove("open");
}

function initBookmarks() {
  // Bookmark toggle button (verse card)
  dom.bookmarkBtn?.addEventListener("click", toggleBookmark);

  // Open modal buttons
  dom.bookmarksToggleBtn?.addEventListener("click", openBookmarksModal);
  dom.bookmarksToggleSidebar?.addEventListener("click", () => {
    closeSidebar();
    setTimeout(openBookmarksModal, 350);
  });

  // Close modal
  dom.bookmarksClose?.addEventListener("click", closeBookmarksModal);
  dom.bookmarksOverlay?.addEventListener("click", closeBookmarksModal);
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && bookmarksPanelOpen) closeBookmarksModal();
  });

  // Clear all bookmarks
  dom.clearBookmarksBtn?.addEventListener("click", () => {
    if (!confirm("Clear all saved verses?")) return;
    saveBookmarksData([]);
    updateBookmarkBtnUI();
    updateBookmarkBadges();
    renderBookmarksList();
    showToast("All saved verses cleared.", "fa-trash");
  });

  // Init badge counts
  updateBookmarkBadges();
  updateBookmarkBtnUI();
}

// ─────────────────────────────────────────────
// 15. CONTACT FORM
// ─────────────────────────────────────────────
function initContactForm() {
  if (!dom.prayerForm) return;
  dom.prayerForm.addEventListener("submit", async e => {
    e.preventDefault();
    const name    = dom.formName?.value.trim()    || "";
    const message = dom.formMessage?.value.trim() || "";

    if (!name) {
      showToast("Please enter your name.", "fa-triangle-exclamation", true);
      dom.formName?.focus(); return;
    }
    if (!message) {
      showToast("Please write a message or prayer request.", "fa-triangle-exclamation", true);
      dom.formMessage?.focus(); return;
    }

    setButtonLoading(dom.submitBtn, true);

    const { error } = await supabase
      .from('prayer_requests')
      .insert([{ name, message }]);

    setButtonLoading(dom.submitBtn, false);

    if (error) {
      showToast('Something went wrong. Please try again.', 'fa-triangle-exclamation', true);
      console.error('Supabase error:', error.message);
      return;
    }

    dom.prayerForm.reset();
    showToast(`Thank you, ${name}! Your prayer has been received. 🙏`, 'fa-hands-praying');
  });
}

// ─────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────
(function init() {
  initDate();
  initDarkMode();
  initScrollProgress();
  initSidebar();
  initActiveNav();
  initHeroParallax();    // Phase 3
  initAnimations();
  initNewVerseButton();
  initCopyButton();
  initShareButton();
  initBookmarks();       // Phase 3
  initContactForm();
  loadVerseOfDay();
})();
