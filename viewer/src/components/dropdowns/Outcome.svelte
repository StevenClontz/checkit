<script lang="ts">
    import {
        UncontrolledDropdown,
        DropdownToggle,
        DropdownMenu,
        DropdownItem,
    } from 'sveltestrap';
    import type { Outcome } from '../../types';
    import { bank } from '../../stores/banks';
    
    export let outcome: Outcome | undefined = undefined;
</script>

<UncontrolledDropdown>
    <DropdownToggle caret>
        {#if outcome}
            {outcome.slug} — {outcome.title}
        {:else}
            Select a learning outcome:
        {/if}
    </DropdownToggle>
    <DropdownMenu>
        {#each $bank.outcomes as o}
            <DropdownItem disabled={o===outcome} href="#/bank/{o.slug}">
                {#if o===outcome}»{/if} {o.slug} — {o.title}
            </DropdownItem>
        {/each}
    </DropdownMenu>
</UncontrolledDropdown>
