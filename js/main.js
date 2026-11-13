/**
 * Main application module.
 * Handles project filtering, contact form validation, and footer year.
 */
(function (global) {
  'use strict';

  /**
   * Initialize project filter buttons.
   */
  function initProjectFilters() {
    const filterButtons = document.querySelectorAll('.projects__filter');
    const projectCards = document.querySelectorAll('.projects__card');

    filterButtons.forEach((button) => {
      // Clone to remove previous listeners when re-initializing after dynamic render.
      const fresh = button.cloneNode(true);
      button.parentNode.replaceChild(fresh, button);
    });

    const buttons = document.querySelectorAll('.projects__filter');
    const cards = document.querySelectorAll('.projects__card');

    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        const filter = button.dataset.filter;

        buttons.forEach((btn) => btn.classList.remove('active'));
        button.classList.add('active');

        cards.forEach((card) => {
          const category = card.dataset.category;
          if (filter === 'all' || category === filter) {
            card.classList.remove('hidden');
            card.style.animation = 'none';
            card.offsetHeight; // eslint-disable-line no-unused-expressions
            card.style.animation = '';
          } else {
            card.classList.add('hidden');
          }
        });
      });
    });
  }

  global.reinitProjectFilters = initProjectFilters;

  /**
   * Initialize contact form validation and API submission.
   */
  function initContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    const fields = ['name', 'email', 'subject', 'message'];
    const submitButton = form.querySelector('.contact__submit');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      let isValid = true;

      fields.forEach((fieldName) => {
        const input = form.elements[fieldName];
        const errorEl = document.getElementById(`${fieldName}Error`);
        const value = input.value.trim();
        let errorMessage = '';

        if (!value) {
          errorMessage = `${capitalize(fieldName)} is required.`;
        } else if (fieldName === 'email' && !isValidEmail(value)) {
          errorMessage = 'Please enter a valid email address.';
        }

        if (errorMessage) {
          isValid = false;
          input.classList.add('error');
        } else {
          input.classList.remove('error');
        }

        errorEl.textContent = errorMessage;
      });

      const successEl = document.getElementById('formSuccess');
      if (!isValid) {
        successEl.textContent = '';
        return;
      }

      const payload = {
        name: form.elements.name.value.trim(),
        email: form.elements.email.value.trim(),
        subject: form.elements.subject.value.trim(),
        message: form.elements.message.value.trim(),
      };

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';
      }
      successEl.textContent = '';

      try {
        if (!global.PortfolioAPI) {
          throw new Error('API client is not available.');
        }
        const result = await global.PortfolioAPI.submitContact(payload);
        successEl.textContent = result.message || 'Thanks for reaching out! I will get back to you soon.';
        successEl.style.color = '';
        form.reset();
        fields.forEach((fieldName) => {
          form.elements[fieldName].classList.remove('error');
          document.getElementById(`${fieldName}Error`).textContent = '';
        });
      } catch (error) {
        successEl.textContent = error.message || 'Sorry, something went wrong. Please try again later.';
        successEl.style.color = 'var(--color-error, #e74c3c)';
      } finally {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = 'Send Message';
        }
      }
    });

    // Clear errors on input.
    fields.forEach((fieldName) => {
      const input = form.elements[fieldName];
      input.addEventListener('input', () => {
        input.classList.remove('error');
        document.getElementById(`${fieldName}Error`).textContent = '';
      });
    });
  }

  /**
   * Validate an email address format.
   * @param {string} email
   * @returns {boolean}
   */
  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  /**
   * Capitalize the first letter of a string.
   * @param {string} str
   * @returns {string}
   */
  function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  /**
   * Set the current year in the footer.
   */
  function setFooterYear() {
    const yearEl = document.getElementById('year');
    if (yearEl) {
      yearEl.textContent = new Date().getFullYear();
    }
  }

  function boot() {
    initProjectFilters();
    initContactForm();
    setFooterYear();
  }

  // Initialize when DOM is ready.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})(window);
