<script>
	import '@picocss/pico/css/pico.min.css';
	import { auth, fetchMe, logout } from '$lib/auth.svelte.js';
	import { goto } from '$app/navigation';

	let { children } = $props();

	// Restore session on app start if a token exists
	$effect(() => {
		if (auth.token && !auth.user) fetchMe();
	});

	function handleLogout() {
		logout();
		goto('/login');
	}
</script>

<nav class="container">
	<ul>
		<li><strong><a href="/">App</a></strong></li>
	</ul>
	<ul>
		{#if auth.token}
			<li><a href="/dashboard">Dashboard</a></li>
			<li><button class="secondary" onclick={handleLogout}>Log out</button></li>
		{:else}
			<li><a href="/login">Log in</a></li>
			<li><a href="/register" role="button">Sign up</a></li>
		{/if}
	</ul>
</nav>

<main class="container">
	{@render children()}
</main>
