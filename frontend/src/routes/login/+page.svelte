<script>
	import { auth, login } from '$lib/auth.svelte.js';
	import { goto } from '$app/navigation';

	let username = $state('');
	let password = $state('');

	async function submit(e) {
		e.preventDefault();
		if (await login(username, password)) goto('/dashboard');
	}
</script>

<article style="max-width: 28rem; margin-inline: auto;">
	<hgroup>
		<h2>Log in</h2>
		<p>Demo user: <code>demo</code> / <code>demo1234</code></p>
	</hgroup>

	<form onsubmit={submit}>
		<label>
			Username
			<input type="text" bind:value={username} autocomplete="username" required />
		</label>
		<label>
			Password
			<input type="password" bind:value={password} autocomplete="current-password" required />
		</label>

		{#if auth.error}
			<p><mark>{auth.error}</mark></p>
		{/if}

		<button type="submit" aria-busy={auth.loading} disabled={auth.loading}>Log in</button>
	</form>

	<p>No account? <a href="/register">Sign up</a></p>
</article>
