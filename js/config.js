/**
 * API configuration.
 * Empty base URL uses the same origin when FastAPI serves the frontend.
 * Override via window.__API_BASE_URL__ if serving static files separately.
 */
(function (global) {
  'use strict';

  const configured = typeof global.__API_BASE_URL__ === 'string'
    ? global.__API_BASE_URL__
    : '';

  global.PortfolioConfig = {
    API_BASE_URL: configured.replace(/\/$/, ''),
  };
})(window);
