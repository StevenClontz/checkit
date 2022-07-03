<script lang="ts">
    import 'bootstrap/dist/css/bootstrap.min.css';
    import 'katex/dist/katex.min.css';
    import { onMount } from 'svelte';
    import { bank } from './stores/banks';
    import Router, { querystring } from 'svelte-spa-router';
    import { routes } from './routes';
    import { Spinner } from 'sveltestrap';
    import CodeCell from './components/CodeCell.svelte';
    import Nav from './components/Nav.svelte';

    let loading = true;
    onMount(async () => {
        const bankFetch = await fetch(
            window['bankJsonUrl']
        );
        bank.set(
            await bankFetch.json(),
        )
        loading = false;
    });

</script>

{#if $querystring != "embed"}
<Nav/>
{/if}

<CodeCell/>

{#if loading}
    <div class="text-center">
        <h1 class="display-4">Loading ☑️It...</h1>
        <Spinner color="primary" />
    </div>
{:else}
    <Router {routes}/>

    <footer>
        <p class="text-center text-muted">
            <small>
                <em>
                    Randomized exericse bank powered by
                    <a target="_blank" href="https://checkit.clontz.org">CheckIt</a>
                    v0.2.3a0
                </em>
            </small>
        </p>
    </footer>
{/if}

<style>
    h1 { margin-top: 1em; }
    footer { margin-top: 2em; }
</style>
