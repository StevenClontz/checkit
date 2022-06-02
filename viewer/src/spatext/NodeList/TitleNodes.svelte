<script lang="ts">
    import Math from '../Elements/Math.svelte';
    export let nodes:NodeList;
</script>

{#each nodes as node}
    {#if node.nodeType == Node.TEXT_NODE}
        {node.textContent}
    {:else if node instanceof Element}
        {#if node.nodeName.toLowerCase() == "m"}
            <Math latex={node.textContent}/>
        {:else if node.nodeName.toLowerCase() == "c"}
            <code>{node.textContent}</code>
        {:else if node.nodeName.toLowerCase() == "em"}
            <em><svelte:self nodes={node.childNodes}/></em>
        {:else if node.nodeName.toLowerCase() == "q"}
            "<svelte:self nodes={node.childNodes}/>"
        {/if}
    {/if}
{/each}