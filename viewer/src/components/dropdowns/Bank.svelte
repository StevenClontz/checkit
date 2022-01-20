<script lang="ts">
    import {
        UncontrolledDropdown,
        DropdownToggle,
        DropdownMenu,
        DropdownItem,
    } from 'sveltestrap';
    import { banks } from '../../stores/banks';
    import type { Bank } from '../../types';

    export let inNav: boolean = false;
    export let bank: Bank | undefined = undefined;
</script>

<UncontrolledDropdown nav={inNav} inNavbar={inNav}>
    <DropdownToggle nav={inNav} caret>
        {#if bank}
            {bank.title}
        {:else}
            {#if inNav}
                Exercise Banks
            {:else}
                Select an exercise bank:
            {/if}
        {/if}
    </DropdownToggle>
    <DropdownMenu>
        {#each $banks as b}
            <DropdownItem disabled={b===bank} href="#/banks/{b.slug}">
                {#if b===bank}»{/if} {b.title}
            </DropdownItem>
        {/each}
        {#if bank}
            {#if $banks.length > 1}
                <DropdownItem divider/>
            {/if}
            <DropdownItem href="#/">Back to Home</DropdownItem>
        {/if}
    </DropdownMenu>
</UncontrolledDropdown>