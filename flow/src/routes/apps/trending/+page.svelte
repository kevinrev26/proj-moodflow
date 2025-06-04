<script lang="ts">
  import { onMount } from 'svelte';

  let loading = true;
  let error: string | null = null;
  let apps: any[] = [];

  onMount(async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/apps/trending/');
      if (!res.ok) throw new Error("Error fetching trending apps");
      const data = await res.json();
      apps = data.top_apps;
    } catch (err) {
      error = (err as Error).message;
    } finally {
      loading = false;
    }
  });
</script>

{#if loading}
  <p>Loading top trending apps...</p>
{:else if error}
  <p>Error: {error}</p>
{:else}
  <section>
    <h2>🔥 Top Trending Apps</h2>
    <ul class="app-list">
      {#each apps as app}
        <li class="app-card">
          <div class="header">
            <h3>{app.title}</h3>
            <span class="score">Trend Score: {app.trend_score.toFixed(2)}</span>
          </div>
          <p><strong>Category:</strong> {app.category} | <strong>Top Type:</strong> {app.top_type}</p>
          <p><strong>Installs:</strong> {app.installs} | <strong>Rating:</strong> {app.score.toFixed(2)} ({app.ratings} ratings)</p>
          <p><strong>Rank:</strong> {app.previous_rank} → {app.current_rank}</p>
        </li>
      {/each}
    </ul>
  </section>
{/if}

<style>
  h2 {
    color: #38bdf8;
    margin-bottom: 1.5rem;
  }

  .app-list {
    list-style: none;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.25rem;
  }

  .app-card {
    background: #1e293b;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }

  .score {
    background: #174e2a;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
  }

  p {
    margin: 0.4rem 0;
  }
</style>
