<script lang="ts">
  import { onMount } from 'svelte';
  import AppHeader from '$lib/components/details/AppDetailHeader.svelte';
  import AppSnapshotTable from '$lib/components/details/AppSnapshotTable.svelte';

  import { page } from '$app/stores';
  import { get } from 'svelte/store';

  let app_id = get(page).params.app_id;
  let loading = true;
  let error: string | null = null;

  let app = null;
  let snapshots = [];
  let description = '';
  let icon_url = '';

  onMount(async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/app/${app_id}/`);
      if (!res.ok || res.status === 204) throw new Error('App not found');
      const data = await res.json();

      app = data.app;
      snapshots = data.snapshots;
      description = data.description;
      icon_url = data.icon_url;
    } catch (err) {
      error = (err as Error).message;
    } finally {
      loading = false;
    }
  });
</script>

{#if loading}
  <p>Loading app details...</p>
{:else if error}
  <p class="error">{error}</p>
{:else}
  <section class="app-details">
    <AppHeader {app} {icon_url} {description} />
    <h3>📈 Snapshot History</h3>
    <AppSnapshotTable {snapshots} />
  </section>
{/if}

<style>
  .app-details {
    padding-bottom: 2rem;
  }

  h3 {
    margin-top: 2rem;
    color: #38bdf8;
  }

  .error {
    color: red;
  }
</style>
