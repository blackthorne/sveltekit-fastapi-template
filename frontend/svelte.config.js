import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// adapter-static + fallback = SPA mode.
		// This is what makes the app Tauri-compatible: the build output in
		// `build/` is plain static files that Tauri can serve directly.
		adapter: adapter({
			fallback: 'index.html'
		})
	}
};

export default config;
