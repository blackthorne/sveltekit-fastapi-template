// Minimal fetch wrapper for the FastAPI backend.
//
// The base URL comes from VITE_API_URL (.env). In a Tauri build the frontend
// is served from tauri://localhost (or http://tauri.localhost on Windows),
// so the API URL must be absolute — never rely on same-origin requests.

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const TOKEN_KEY = 'access_token';

export function getToken() {
	if (typeof localStorage === 'undefined') return null;
	return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
	localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
	localStorage.removeItem(TOKEN_KEY);
}

/**
 * @param {string} path - e.g. '/users/me'
 * @param {{method?: string, body?: object, headers?: object}} [options]
 */
export async function api(path, { method = 'GET', body, headers = {} } = {}) {
	const token = getToken();

	const res = await fetch(`${BASE_URL}${path}`, {
		method,
		headers: {
			...(body ? { 'Content-Type': 'application/json' } : {}),
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...headers
		},
		body: body ? JSON.stringify(body) : undefined
	});

	if (!res.ok) {
		let detail = res.statusText;
		try {
			const data = await res.json();
			detail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
		} catch {
			/* non-JSON error body */
		}
		throw new Error(detail);
	}

	if (res.status === 204) return null;
	return res.json();
}
