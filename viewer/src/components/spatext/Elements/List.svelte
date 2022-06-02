<script lang="ts">
    import ContentNodes from '../NodeList/ContentNodes.svelte'
    export let list:Element;
</script>

{#if list.querySelector('item')}
<ul>
    {#each list.children as item}
        {#if item.tagName.toLowerCase()=="item"}
            <li><ContentNodes nodes={item.childNodes}/></li>
        {/if}
    {/each}
</ul>
{/if}