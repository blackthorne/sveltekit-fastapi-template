<script>
	import { auth } from '$lib/auth.svelte.js';
</script>

<hgroup>
	<h1>SvelteKit + FastAPI template</h1>
	<p>Svelte 5 · Pico CSS · JWT auth · Tauri-ready</p>
</hgroup>

{#if auth.user}
	<p>Signed in as <strong>{auth.user.username}</strong>. Head to your <a href="/dashboard">dashboard</a>.</p>
{:else}
	<p><a href="/login" role="button">Log in</a> or <a href="/register">create an account</a> to try the protected area.</p>
{/if}
