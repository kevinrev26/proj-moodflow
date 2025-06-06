<script lang="ts">
    import { onMount } from 'svelte';

    let loading = true;
    let error = null;
    let summary = null;

    onMount(async () => {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/v1/summary/');
            if (!res.ok) throw new Error("Error fetching summary");
            summary = await res.json();
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    });
</script>

    {#if loading}
        <p>Loading summary...</p>
    {:else if error}
        <p>Error: {error}</p>
    {:else}
    <section>
        <h2>📊 MoodFlow Summary</h2>
        <p><strong>Total apps tracked:</strong> {summary.total_apps_tracked}</p>
        <p><strong>Categories monitored:</strong> {summary.categories_monitored}</p>

        <h3>🔥 Active Categories</h3>
        <ul>
        {#each summary.active_categories as cat}
            <li>{cat}</li>
        {/each}
        </ul>

        <h3>📈 Top 5 Trending Apps</h3>
        <ol>
        {#each summary.apps_most_trend_scores as app}
            <li>
                <a  href={`/app/${app.app_id}`} class="card-link">
                    <strong>{app.title}</strong> ({app.category}, {app.top_type})<br />
                </a>
                Trend Score: {app.trend_score.toFixed(2)}<br />
                Installs: {app.installs} | Rating: {app.score != null ? app.score.toFixed(2) : ''} ({app.ratings} ratings)
            </li>
        {/each}
        </ol>
    </section>
    {/if}

<style>
    h2, h3 {
        margin-top: 1.5rem;
        color: #38bdf8;
    }

    ul, ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }

    li {
        margin-bottom: 0.75rem;
    }
</style>
