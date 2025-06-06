<script lang="ts">
  export let snapshots: any[];
</script>

<table class="snapshot-table">
  <thead>
    <tr>
      <th>Date</th>
      <th>Top Type</th>
      <th>Rank (Prev → Curr)</th>
      <th>Trend Score</th>
      <th>Rating</th>
      <th>Total Ratings</th>
    </tr>
  </thead>
  <tbody>
    {#each snapshots as snap}
      <tr>
        <td>{new Date(snap.snapshot_time).toLocaleString()}</td>
        <td>{snap.top_type}</td>
        <td>{snap.previous_rank} → {snap.current_rank}</td>
        <td>{snap.trend_score.toFixed(2)}</td>
        <td>{snap.score ?? 'N/A'}</td>
        <td>{snap.ratings ?? 'N/A'}</td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  .snapshot-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }

  th, td {
    border: 1px solid #334155;
    padding: 0.5rem;
    text-align: center;
  }

  thead {
    background: #1e293b;
    color: #fff;
  }

  tbody tr:nth-child(even) {
    background: #0f172a;
  }
</style>
