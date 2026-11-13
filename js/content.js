/**
 * Load portfolio content from the API and render into existing sections.
 * Keeps current HTML as a fallback when the API is unavailable.
 */
(function (global) {
  'use strict';

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderProfile(profile) {
    const heroTitle = document.getElementById('heroTitle');
    if (heroTitle) heroTitle.textContent = profile.name;

    const typing = document.getElementById('typingText');
    if (typing && profile.typing_roles) {
      typing.dataset.roles = profile.typing_roles;
    }

    const heroDescription = document.querySelector('.hero__description');
    if (heroDescription) heroDescription.textContent = profile.tagline;

    const logo = document.querySelector('.nav__logo');
    if (logo) {
      const firstName = profile.name.split(' ')[0] || profile.name;
      logo.innerHTML =
        `<span class="nav__logo-bracket">&lt;</span>${escapeHtml(firstName)}` +
        `<span class="nav__logo-bracket">/&gt;</span>`;
      logo.setAttribute('aria-label', `${profile.name} home`);
    }

    document.title = `${profile.name} | ${profile.title}`;

    const aboutHeading = document.querySelector('.about__heading');
    if (aboutHeading) aboutHeading.textContent = profile.bio_heading;

    const aboutTexts = document.querySelectorAll('.about__text');
    if (aboutTexts[0]) aboutTexts[0].textContent = profile.bio_paragraph_1;
    if (aboutTexts[1]) aboutTexts[1].textContent = profile.bio_paragraph_2;

    const initials = document.querySelector('.about__image-text');
    if (initials) initials.textContent = profile.initials || profile.name.slice(0, 2).toUpperCase();

    const aboutImage = document.querySelector('.about__image');
    if (aboutImage) {
      aboutImage.setAttribute('aria-label', `${profile.name} profile photo placeholder`);
    }

    const stats = [
      { selector: '.about__stat-number[data-target]', value: profile.years_experience, index: 0 },
      { selector: '.about__stat-number[data-target]', value: profile.projects_shipped, index: 1 },
      { selector: '.about__stat-number[data-target]', value: profile.teams_led, index: 2 },
    ];
    const statNodes = document.querySelectorAll('.about__stat-number[data-target]');
    stats.forEach((stat) => {
      if (statNodes[stat.index]) {
        statNodes[stat.index].dataset.target = String(stat.value);
        statNodes[stat.index].textContent = '0';
      }
    });

    const resumeLink = document.querySelector('.about__content .btn--primary');
    if (resumeLink) {
      resumeLink.href = profile.resume_url || '#';
      if (profile.resume_url && profile.resume_url !== '#') {
        resumeLink.setAttribute('download', '');
      }
    }

    const contactHeading = document.querySelector('.contact__heading');
    if (contactHeading) contactHeading.textContent = profile.contact_heading;

    const contactText = document.querySelector('.contact__text');
    if (contactText) contactText.textContent = profile.contact_text;

    const emailDetail = document.querySelector('.contact__details a.contact__detail');
    if (emailDetail) {
      emailDetail.href = `mailto:${profile.email}`;
      const emailSpan = emailDetail.querySelector('span:last-child');
      if (emailSpan) emailSpan.textContent = profile.email;
    }

    const locationDetail = document.querySelectorAll('.contact__details .contact__detail')[1];
    if (locationDetail) {
      const locationSpan = locationDetail.querySelector('span:last-child');
      if (locationSpan) locationSpan.textContent = profile.location;
    }

    const heroSocials = document.querySelectorAll('.hero__social-link');
    if (heroSocials[0]) heroSocials[0].href = profile.github_url || '#';
    if (heroSocials[1]) heroSocials[1].href = profile.linkedin_url || '#';
    if (heroSocials[2]) heroSocials[2].href = `mailto:${profile.email}`;

    const contactSocials = document.querySelectorAll('.contact__social-link');
    if (contactSocials[0]) contactSocials[0].href = profile.github_url || '#';
    if (contactSocials[1]) contactSocials[1].href = profile.linkedin_url || '#';
    if (contactSocials[2]) contactSocials[2].href = profile.twitter_url || '#';

    const footerCopy = document.querySelector('.footer__copy');
    if (footerCopy) {
      footerCopy.innerHTML =
        `© <span id="year"></span> ${escapeHtml(profile.name)}. All rights reserved.`;
      const yearEl = document.getElementById('year');
      if (yearEl) yearEl.textContent = String(new Date().getFullYear());
    }

    const codeName = document.querySelector('.hero__code-string');
    if (codeName) codeName.textContent = `"${profile.name}"`;
  }

  function renderSkills(categories) {
    const grid = document.querySelector('.skills__grid');
    if (!grid || !categories.length) return;

    grid.innerHTML = categories
      .map(
        (category) => `
      <article class="skills__card">
        <div class="skills__card-icon" aria-hidden="true">${escapeHtml(category.icon)}</div>
        <h3 class="skills__card-title">${escapeHtml(category.title)}</h3>
        <ul class="skills__list">
          ${(category.skills || [])
            .map((skill) => `<li class="skills__item">${escapeHtml(skill.name)}</li>`)
            .join('')}
        </ul>
      </article>`
      )
      .join('');
  }

  function renderExperience(items) {
    const timeline = document.querySelector('.experience__timeline');
    if (!timeline || !items.length) return;

    timeline.innerHTML = items
      .map(
        (item) => `
      <article class="experience__item">
        <div class="experience__marker" aria-hidden="true"></div>
        <div class="experience__content">
          <span class="experience__date">${escapeHtml(item.date_range)}</span>
          <h3 class="experience__role">${escapeHtml(item.role)}</h3>
          <p class="experience__company">${escapeHtml(item.company)}</p>
          <ul class="experience__details">
            ${(item.details || [])
              .map((detail) => `<li>${escapeHtml(detail)}</li>`)
              .join('')}
          </ul>
        </div>
      </article>`
      )
      .join('');
  }

  function renderProjects(projects) {
    const grid = document.querySelector('.projects__grid');
    if (!grid || !projects.length) return;

    grid.innerHTML = projects
      .map((project) => {
        const imageInner = project.image_url
          ? `<img src="${escapeHtml(project.image_url)}" alt="${escapeHtml(project.title)}">`
          : `<span class="projects__card-placeholder">${escapeHtml(project.image_label || project.title)}</span>`;

        return `
      <article class="projects__card" data-category="${escapeHtml(project.category)}">
        <div class="projects__card-image" role="img" aria-label="${escapeHtml(project.image_label || project.title)}">
          ${imageInner}
        </div>
        <div class="projects__card-body">
          <h3 class="projects__card-title">${escapeHtml(project.title)}</h3>
          <p class="projects__card-description">${escapeHtml(project.description)}</p>
          <ul class="projects__card-tech">
            ${(project.tech_stack || [])
              .map((tech) => `<li>${escapeHtml(tech)}</li>`)
              .join('')}
          </ul>
          <div class="projects__card-links">
            <a href="${escapeHtml(project.demo_url || '#')}" class="projects__card-link" target="_blank" rel="noopener noreferrer">${escapeHtml(project.demo_label || 'Live Demo')}</a>
            <a href="${escapeHtml(project.source_url || '#')}" class="projects__card-link" target="_blank" rel="noopener noreferrer">${escapeHtml(project.source_label || 'Source Code')}</a>
          </div>
        </div>
      </article>`;
      })
      .join('');

    if (typeof global.reinitProjectFilters === 'function') {
      global.reinitProjectFilters();
    }
  }

  function renderEducation(items) {
    const grid = document.querySelector('.education__grid');
    if (!grid || !items.length) return;

    grid.innerHTML = items
      .map(
        (item) => `
      <article class="education__card">
        <h3 class="education__degree">${escapeHtml(item.degree)}</h3>
        <p class="education__school">${escapeHtml(item.school)}</p>
        <span class="education__year">${escapeHtml(item.year)}</span>
      </article>`
      )
      .join('');
  }

  async function loadContent() {
    if (!global.PortfolioAPI) return;

    try {
      const [profile, skills, experience, projects, education] = await Promise.all([
        global.PortfolioAPI.getProfile(),
        global.PortfolioAPI.getSkills(),
        global.PortfolioAPI.getExperience(),
        global.PortfolioAPI.getProjects(),
        global.PortfolioAPI.getEducation(),
      ]);

      renderProfile(profile);
      renderSkills(skills);
      renderExperience(experience);
      renderProjects(projects);
      renderEducation(education);

      document.dispatchEvent(new CustomEvent('portfolio:content-loaded'));
    } catch (error) {
      console.warn('Unable to load dynamic content from API; using static markup.', error);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadContent);
  } else {
    loadContent();
  }
})(window);
