<script>
	import { auth, fetchMe } from '$lib/auth.svelte.js';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api.js';

	let protectedData = $state(null);
	let error = $state(null);

	// Client-side route guard (SPA — there is no server to guard for us)
	$effect(() => {
		if (!auth.token) goto('/login');
	});

	async function loadProtected() {
		error = null;
		try {
			protectedData = await api('/protected/ping');
		} catch (e) {
			error = e.message;
		}
	}
</script>

{#if auth.user}
	<hgroup>
		<h2>Dashboard</h2>
		<p>Only visible with a valid JWT.</p>
	</hgroup>

	<article>
		<header><strong>Your profile</strong> (from <code>GET /users/me</code>)</header>
		<pre>{JSON.stringify(auth.user, null, 2)}</pre>
	</article>

	<article>
		<header><strong>Protected endpoint test</strong></header>
		<button onclick={loadProtected}>Call <code>GET /protected/ping</code></button>
		{#if protectedData}
			<pre>{JSON.stringify(protectedData, null, 2)}</pre>
		{/if}
		{#if error}
			<p><mark>{error}</mark></p>
		{/if}
	</article>
{:else}
	<p aria-busy="true">Loading…</p>
{/if}
