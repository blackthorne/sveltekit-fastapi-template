// SPA mode: no server-side rendering anywhere.
// Required for adapter-static's `fallback` option and for Tauri,
// where there is no Node server at runtime.
export const ssr = false;
export const prerender = false;
