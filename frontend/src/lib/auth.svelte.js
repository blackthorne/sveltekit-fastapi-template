// Global auth state using Svelte 5 runes (.svelte.js module).
//
// The JWT is kept in localStorage so the session survives reloads.
// This also works inside a Tauri webview. If you later add highly
// sensitive data, consider the tauri-plugin-store or OS keychain
// (tauri-plugin-keyring) instead of localStorage for the desktop build.

import { api, setToken, clearToken, getToken } from '$lib/api.js';

export const auth = $state({
	user: null,
	token: getToken(),
	loading: false,
	error: null
});

export async function login(username, password) {
	auth.loading = true;
	auth.error = null;
	try {
		const data = await api('/auth/login', {
			method: 'POST',
			body: { username, password }
		});
		setToken(data.access_token);
		auth.token = data.access_token;
		await fetchMe();
		return true;
	} catch (e) {
		auth.error = e.message;
		return false;
	} finally {
		auth.loading = false;
	}
}

export async function register(username, password) {
	auth.loading = true;
	auth.error = null;
	try {
		await api('/auth/register', {
			method: 'POST',
			body: { username, password }
		});
		// Auto-login after successful registration
		return await login(username, password);
	} catch (e) {
		auth.error = e.message;
		return false;
	} finally {
		auth.loading = false;
	}
}

export async function fetchMe() {
	if (!auth.token) return;
	try {
		auth.user = await api('/users/me');
	} catch {
		// Token expired or invalid
		logout();
	}
}

export function logout() {
	clearToken();
	auth.token = null;
	auth.user = null;
}
