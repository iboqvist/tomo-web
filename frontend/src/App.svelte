<script lang="ts">
  type Session = { id: string; started_at: string; duration_sec: number };

  const WORK_SEC = 25 * 60;

  let sessions = $state<Session[]>([]);
  let startedAt = $state<number | null>(null);
  let now = $state(Date.now());
  let error = $state('');

  const remaining = $derived(
    startedAt === null ? WORK_SEC : Math.max(0, WORK_SEC - Math.floor((now - startedAt) / 1000))
  );
  const clock = $derived(
    `${String(Math.floor(remaining / 60)).padStart(2, '0')}:${String(remaining % 60).padStart(2, '0')}`
  );

  async function api<T>(path: string, body: unknown = undefined): Promise<T> {
    const response = await fetch(`/api${path}`, {
      method: body ? 'POST' : 'GET',
      headers: body ? { 'Content-Type': 'application/json' } : {},
      body: body ? JSON.stringify(body) : undefined
    });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return response.json();
  }

  async function load() {
    try {
      sessions = await api<Session[]>('/sessions');
      error = '';
    } catch (e) {
      error = `Could not reach the API (${(e as Error).message})`;
    }
  }

  function start() {
    startedAt = now = Date.now();
  }

  async function stop() {
    if (startedAt === null) return;
    const session = { started_at: new Date(startedAt).toISOString(), duration_sec: WORK_SEC - remaining };
    startedAt = null;
    try {
      await api('/sessions', session);
      await load();
    } catch (e) {
      error = `Session not saved (${(e as Error).message})`;
    }
  }

  $effect(() => {
    const interval = setInterval(() => (now = Date.now()), 250);
    return () => clearInterval(interval);
  });

  $effect(() => {
    if (startedAt !== null && remaining === 0) stop();
  });

  load();
</script>

<main>
  <h1>Tomo</h1>
  <div class="clock">{clock}</div>
  {#if startedAt === null}
    <button onclick={start}>Start</button>
  {:else}
    <button onclick={stop}>Stop</button>
  {/if}

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <h2>Sessions</h2>
  {#if sessions.length === 0}
    <p>No sessions yet.</p>
  {:else}
    <ul>
      {#each sessions as session (session.id)}
        <li>
          <span>{new Date(session.started_at).toLocaleString()}</span>
          <span>{Math.round(session.duration_sec / 60)} min</span>
        </li>
      {/each}
    </ul>
  {/if}
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: system-ui, sans-serif;
    background: #f6f7fb;
    color: #0f1219;
  }
  @media (prefers-color-scheme: dark) {
    :global(body) {
      background: #12141a;
      color: #e8eaf0;
    }
  }
  main {
    max-width: 28rem;
    margin: 0 auto;
    padding: 3rem 1rem;
    text-align: center;
  }
  .clock {
    font-size: 4rem;
    font-variant-numeric: tabular-nums;
    margin: 1rem 0;
  }
  button {
    font: inherit;
    padding: 0.5rem 2rem;
    border: none;
    border-radius: 999px;
    background: #2b6cff;
    color: white;
    cursor: pointer;
  }
  .error {
    color: #d33;
  }
  ul {
    list-style: none;
    padding: 0;
    text-align: left;
  }
  li {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #8884;
  }
</style>
