<script lang="ts">
    import Paragraph from '../Elements/Paragraph.svelte'
    import Knowl from '../Elements/Knowl.svelte'
    import List from '../Elements/List.svelte'
    export let nodes:NodeList
    export let allowKnowls=false
</script>

{#each nodes as node}
    {#if node instanceof Element}
        {#if node.nodeName.toLowerCase() == "p"}
            <Paragraph paragraph={node}/>
        {:else if node.nodeName.toLowerCase() == "list"}
            <List list={node}/>
        {:else if node.nodeName.toLowerCase() == "knowl" && allowKnowls}
            <Knowl knowl={node}/>
        {/if}
    {/if}
{/each}