/**
 * Navigation module.
 * Handles sticky header, mobile menu toggle, smooth scrolling,
 * and active section highlighting.
 */
(function () {
  'use strict';

  const header = document.getElementById('header');
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav__link');
  const sections = document.querySelectorAll('section[id]');

  /**
   * Toggle the mobile navigation menu.
   */
  function toggleMobileMenu() {
    const isOpen = navMenu.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
    document.body.style.overflow = isOpen ? 'hidden' : '';
  }

  /**
   * Close the mobile navigation menu.
   */
  function closeMobileMenu() {
    navMenu.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  /**
   * Update header styling on scroll.
   */
  function handleScroll() {
    if (window.scrollY > 20) {
      header.classList.add('header--scrolled');
    } else {
      header.classList.remove('header--scrolled');
    }

    highlightActiveSection();
  }

  /**
   * Highlight the nav link corresponding to the current section.
   */
  function highlightActiveSection() {
    const scrollPos = window.scrollY + header.offsetHeight + 100;

    sections.forEach((section) => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach((link) => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  // Event listeners
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', toggleMobileMenu);
  }

  navLinks.forEach((link) => {
    link.addEventListener('click', (event) => {
      closeMobileMenu();

      const href = link.getAttribute('href');
      if (href.startsWith('#')) {
        event.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          const offset = header ? header.offsetHeight : 0;
          const top = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
        }
      }
    });
  });

  window.addEventListener('scroll', handleScroll, { passive: true });
  window.addEventListener('resize', closeMobileMenu);

  // Initial calls
  handleScroll();
})();
