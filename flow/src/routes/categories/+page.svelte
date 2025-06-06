<script lang="ts">
  import { onMount } from 'svelte';

  let categories: string[] = [];
  let selectedCategory = '';
  let loading = false;
  let error: string | null = null;

  let apps = {
    top_free: [],
    top_grossing: [],
    top_paid: []
  };

  let activeTab: keyof typeof apps = 'top_free';

  async function fetchCategoryData(category: string) {
    if (!category) return;
    loading = true;
    error = null;

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/category/${category}/`);
      if (!res.ok) throw new Error("Error fetching category");
      const data = await res.json();

      // separa apps por tipo
      apps.top_free = data.top.filter((a) => a.top_type === 'top_free');
      apps.top_grossing = data.top.filter((a) => a.top_type === 'top_grossing');
      apps.top_paid = data.top.filter((a) => a.top_type === 'top_paid');
    } catch (err) {
      error = (err as Error).message;
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/summary/');
      const data = await res.json();
      categories = data.categories;
      selectedCategory = categories[0];
      await fetchCategoryData(selectedCategory);
    } catch (err) {
      error = 'Error loading categories';
    }
  });

  $: if (selectedCategory) fetchCategoryData(selectedCategory);
</script>

<section>
  <h2>📂 Categories</h2>

  <label>
    Select category:
    <select bind:value={selectedCategory}>
      {#each categories as category}
        <option value={category}>{category}</option>
      {/each}
    </select>
  </label>

  <div class="tabs">
    <button on:click={() => (activeTab = 'top_free')} class:active={activeTab === 'top_free'}>Top Free</button>
    <button on:click={() => (activeTab = 'top_grossing')} class:active={activeTab === 'top_grossing'}>Top Grossing</button>
    <button on:click={() => (activeTab = 'top_paid')} class:active={activeTab === 'top_paid'}>Top Paid</button>
  </div>

  {#if loading}
    <p>Loading apps...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else}
    <ul class="app-list">
      {#each apps[activeTab] as app}
        <li class="app-card">
          <a href={`/app/${app.app_id}`} class="card-link">
            <div class="header">
              <h3>{app.title}</h3>
              <span class="score">{app.trend_score.toFixed(2)}</span>
            </div>
            <p><strong>Rank:</strong> {app.previous_rank} → {app.current_rank}</p>
            <p><strong>Installs:</strong> {app.installs} | Rating: {app.score ?? 'N/A'}</p>
          </a>
        </li>
      {/each}
    </ul>
  {/if}
</section>

<style>
  section {
    padding-bottom: 3rem;
  }

  label {
    margin-top: 1rem;
    display: block;
  }

  select {
    margin-left: 1rem;
    padding: 0.4rem;
    font-size: 1rem;
  }

  .tabs {
    margin-top: 2rem;
    margin-bottom: 1rem;
  }

  button {
    margin-right: 1rem;
    padding: 0.5rem 1rem;
    background-color: #1e293b;
    color: #fff;
    border: none;
    cursor: pointer;
    border-radius: 4px;
  }

  button.active {
    background-color: #38bdf8;
    color: #0f172a;
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
    background: #22c55e;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
  }
</style>
