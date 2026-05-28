// static/js/search.js
// Live search/filter for dashboard tables.
// Filters table rows instantly as the user types.
// No server request needed — filters the already-loaded HTML.

/**
 * Filter a table's rows based on search text.
 *
 * @param {string} tableId     - The id of the <table> element
 * @param {string} searchText  - The text to search for
 *
 * How it works:
 * 1. Get all <tr> rows in the table body
 * 2. For each row, get all its text content
 * 3. If the row's text includes the search term → show it
 * 4. If not → hide it
 *
 * Usage (from HTML):
 *   <input oninput="searchTable('users-table', this.value)" />
 */
function searchTable(tableId, searchText) {
  const table = document.getElementById(tableId);
  if (!table) return;

  // Get all rows in the table body (not the header)
  const rows = table.querySelectorAll('tbody tr');

  // Normalize: lowercase for case-insensitive comparison
  const query = searchText.toLowerCase().trim();

  let visibleCount = 0;

  rows.forEach(function (row) {
    // Get all text in this row, combined into one string
    const rowText = row.textContent.toLowerCase();

    if (query === '' || rowText.includes(query)) {
      // Show this row
      row.style.display = '';
      visibleCount++;
    } else {
      // Hide this row
      row.style.display = 'none';
    }
  });

  // Show "no results" message if nothing matches
  showNoResultsMessage(table, visibleCount, query);
}

/**
 * Show or hide a "no results" row based on search results.
 */
function showNoResultsMessage(table, visibleCount, query) {
  // Look for an existing "no results" row
  let noResultsRow = table.querySelector('.no-results-row');

  if (visibleCount === 0 && query !== '') {
    if (!noResultsRow) {
      // Count columns to know how wide to span
      const colCount = table.querySelectorAll('thead th').length || 5;

      noResultsRow = document.createElement('tr');
      noResultsRow.className = 'no-results-row';
      noResultsRow.innerHTML = `
        <td colspan="${colCount}"
            class="px-6 py-8 text-center text-gray-400 text-sm">
          No results found for "<strong>${query}</strong>"
        </td>
      `;
      table.querySelector('tbody').appendChild(noResultsRow);
    }
  } else {
    if (noResultsRow) noResultsRow.remove();
  }
}
