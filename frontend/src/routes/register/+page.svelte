<script>
	import { auth, register } from '$lib/auth.svelte.js';
	import { goto } from '$app/navigation';

	let username = $state('');
	let password = $state('');

	async function submit(e) {
		e.preventDefault();
		if (await register(username, password)) goto('/dashboard');
	}
</script>

<article style="max-width: 28rem; margin-inline: auto;">
	<h2>Create account</h2>

	<form onsubmit={submit}>
		<label>
			Username
			<input type="text" bind:value={username} autocomplete="username" minlength="3" required />
		</label>
		<label>
			Password
			<input
				type="password"
				bind:value={password}
				autocomplete="new-password"
				minlength="8"
				maxlength="72"
				required
			/>
		</label>

		{#if auth.error}
			<p><mark>{auth.error}</mark></p>
		{/if}

		<button type="submit" aria-busy={auth.loading} disabled={auth.loading}>Sign up</button>
	</form>

	<p>Already registered? <a href="/login">Log in</a></p>
</article>
