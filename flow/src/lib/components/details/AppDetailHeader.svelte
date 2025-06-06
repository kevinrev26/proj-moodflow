<script lang="ts">
  export let app;
  export let icon_url: string;
  export let description: string;
</script>

<div class="header-container">
  <img src={icon_url} alt={app.title} class="icon" />
  <div class="info">
    <h1>{app.title}</h1>
    <p class="category">📂 {app.category}</p>
    <p class="description">{description}</p>
  </div>
</div>

<style>
  .header-container {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 2rem;
  }

  .icon {
    width: 72px;
    height: 72px;
    border-radius: 12px;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
  }

  .info {
    flex: 1;
  }

  h1 {
    margin: 0;
    font-size: 1.8rem;
  }

  .category {
    color: #a1a1aa;
    margin-top: 0.3rem;
  }

  .description {
    margin-top: 0.5rem;
    font-size: 0.95rem;
    line-height: 1.5;
  }
</style>
