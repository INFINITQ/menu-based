// static/js/app.js - minimal glue; most pages include inline scripts for page-specific logic
(function () {
  console.log('Mega Tool app.js loaded');

  // Helpful helper to fetch JSON (can be extended app-wide)
  window.megaApi = {
    json: async function(path, opts = {}) {
      if (!opts.headers) opts.headers = { 'Content-Type': 'application/json' };
      const res = await fetch(path, opts);
      if (res.headers.get('content-type')?.includes('application/json')) {
        return res.json();
      }
      return res.text();
    }
  };
})();
