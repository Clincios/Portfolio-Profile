/**
 * Animations module.
 * Provides scroll-reveal animations, typing effect, and animated counters.
 */
(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /**
   * Scroll reveal using Intersection Observer.
   */
  function initScrollReveal() {
    const revealElements = document.querySelectorAll(
      '.section__header, .about__grid, .skills__card, .experience__item, .projects__card, .education__card, .contact__grid'
    );

    revealElements.forEach((el, index) => {
      el.classList.add('reveal');
      // Stagger children slightly for visual rhythm.
      el.style.transitionDelay = prefersReducedMotion ? '0s' : `${(index % 4) * 0.05}s`;
    });

    if (prefersReducedMotion) {
      revealElements.forEach((el) => el.classList.add('active'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('active');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    revealElements.forEach((el) => observer.observe(el));
  }

  /**
   * Typing effect for hero role text.
   */
  function initTypingEffect() {
    const typingElement = document.getElementById('typingText');
    if (!typingElement || prefersReducedMotion) {
      if (typingElement) {
        const roles = typingElement.dataset.roles.split(',');
        typingElement.textContent = roles[0];
      }
      return;
    }

    const roles = typingElement.dataset.roles.split(',');
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typeSpeed = 100;
    const deleteSpeed = 50;
    const pauseBetween = 2000;

    function type() {
      const currentRole = roles[roleIndex];

      if (isDeleting) {
        typingElement.textContent = currentRole.substring(0, charIndex - 1);
        charIndex--;
      } else {
        typingElement.textContent = currentRole.substring(0, charIndex + 1);
        charIndex++;
      }

      let nextDelay = isDeleting ? deleteSpeed : typeSpeed;

      if (!isDeleting && charIndex === currentRole.length) {
        nextDelay = pauseBetween;
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        nextDelay = 500;
      }

      setTimeout(type, nextDelay);
    }

    type();
  }

  /**
   * Animate numeric counters when they enter the viewport.
   */
  function initCounters() {
    const counters = document.querySelectorAll('.about__stat-number');
    if (!counters.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const counter = entry.target;
            const target = parseInt(counter.dataset.target, 10);
            animateCounter(counter, target);
            observer.unobserve(counter);
          }
        });
      },
      { threshold: 0.5 }
    );

    counters.forEach((counter) => observer.observe(counter));
  }

  /**
   * Animate a single counter to its target value.
   * @param {HTMLElement} element
   * @param {number} target
   */
  function animateCounter(element, target) {
    const duration = 1500;
    const start = performance.now();

    function update(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      element.textContent = Math.floor(eased * target);

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.textContent = target;
      }
    }

    requestAnimationFrame(update);
  }

  // Initialize animations after DOM is ready.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initScrollReveal();
      initTypingEffect();
      initCounters();
    });
  } else {
    initScrollReveal();
    initTypingEffect();
    initCounters();
  }
})();
