/**
 * Thin fetch wrapper for portfolio API endpoints.
 */
(function (global) {
  'use strict';

  function getBaseUrl() {
    return (global.PortfolioConfig && global.PortfolioConfig.API_BASE_URL) || '';
  }

  async function request(path, options) {
    const url = `${getBaseUrl()}${path}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options && options.headers),
      },
      ...options,
    });

    let data = null;
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      const detail =
        data && typeof data === 'object' && data.detail
          ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
          : `Request failed with status ${response.status}`;
      const error = new Error(detail);
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  }

  global.PortfolioAPI = {
    getProfile() {
      return request('/api/profile');
    },
    getSkills() {
      return request('/api/skills');
    },
    getExperience() {
      return request('/api/experience');
    },
    getProjects(category) {
      const query = category && category !== 'all' ? `?category=${encodeURIComponent(category)}` : '';
      return request(`/api/projects${query}`);
    },
    getEducation() {
      return request('/api/education');
    },
    submitContact(payload) {
      return request('/api/contact', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
    },
  };
})(window);
