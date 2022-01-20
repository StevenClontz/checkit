<script lang="ts">
    import { Alert } from 'sveltestrap';
    import { isOpen } from '../stores/codecell';
    import {toggleCodeCell} from '../utils';
    let loaded:Boolean = false;
    $: if ($isOpen) {
        loaded = true;
    }
</script>

{#if loaded}
<div style="display: {$isOpen ? 'block' : 'none'}">
    <Alert color="secondary">
        <button type="button" class="close" on:click={toggleCodeCell} aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
        <h4>
            Code Cell:
        </h4>
        <iframe title="codecell" style="width:100%;height:50vh;" src="https://checkit.clontz.org/codecell/"/>
    </Alert>
</div>
{/if}