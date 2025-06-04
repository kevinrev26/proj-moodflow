<script>
  import SidebarNavigation from './SidebarNavigation.svelte';
</script>

<div class="layout">
  <SidebarNavigation />
  <main class="main">
    <slot />
  </main>
</div>

<style>
  .layout {
    display: flex;
    min-height: 100vh;
    background-color: #0f172a;
    color: #f1f5f9;
    font-family: system-ui, sans-serif;
  }

  .main {
    flex-grow: 1;
    padding: 2rem;
    overflow-y: auto;
  }
</style>
