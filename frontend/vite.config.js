import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],

	// Tauri expects a fixed port; fail instead of silently picking another one.
	server: {
		port: 5173,
		strictPort: true
	},
	// Don't clutter the terminal Tauri runs the dev server in.
	clearScreen: false
});
