/**
 * Theme toggle module.
 * Handles dark/light mode switching and persists user preference.
 */
(function () {
  'use strict';

  const STORAGE_KEY = 'portfolio-theme';
  const toggleButton = document.getElementById('themeToggle');

  /**
   * Get the initially preferred theme.
   * @returns {string} 'light' or 'dark'
   */
  function getInitialTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  /**
   * Apply the given theme to the document.
   * @param {string} theme
   */
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
  }

  /**
   * Toggle between light and dark themes.
   */
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem(STORAGE_KEY, next);
  }

  // Initialize theme as early as possible to avoid flash.
  applyTheme(getInitialTheme());

  if (toggleButton) {
    toggleButton.addEventListener('click', toggleTheme);
  }
})();
