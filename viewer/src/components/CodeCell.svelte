<script lang="ts">
    import { isOpen } from '../stores/codecell';
    import {toggleCodeCell} from '../utils';

    let loaded:Boolean = false;
    $: if ($isOpen) {
        loaded = true;
    }
</script>

{#if loaded}
    <div role="alert" class="alert alert-secondary alert-dismissible" style="display: {$isOpen ? 'block' : 'none'}">
        <button type="button" class="btn-close" on:click={toggleCodeCell} aria-label="Close"/>
        <h4>
            Code Cell:
        </h4>
        <iframe title="codecell" style="width:100%;height:33vh;" src="https://checkit.clontz.org/codecell/"/>
    </div>
{/if}