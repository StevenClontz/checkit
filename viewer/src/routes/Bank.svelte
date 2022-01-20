<script lang="ts">
    import type {Params, Outcome} from '../types';
    export let params:Params;

    import {
        Container,
        Alert,
    } from 'sveltestrap';
    import OutcomeDropdown from '../components/dropdowns/Outcome.svelte';

    let outcome: Outcome | undefined = undefined;
    $: if (params && params.outcomeSlug) {
        outcome = $bank.outcomes.find((o)=>o.slug==params.outcomeSlug)
    }

    import { querystring } from 'svelte-spa-router';
    import { bank } from '../stores/banks';
</script>

<main>
    <Container>
        <h1>{$bank.title}</h1>
        {#if $bank.outcomes}
            {#if $querystring != "embed"}
                <p>
                    <OutcomeDropdown {outcome}/>
                </p>
            {/if}
        {:else}
            <Alert color="warning">No outcomes found for this bank.</Alert>
        {/if}
        {#if !outcome}
            <p>Homepage: <a href={$bank.url}>{$bank.url}</a></p>
        {/if}
        <slot/>
    </Container>
</main>

<style>
    h1 {margin-top: 0.5em;}
</style>