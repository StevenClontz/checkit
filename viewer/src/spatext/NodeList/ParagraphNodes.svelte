<script lang="ts">
    import Math from '../Elements/Math.svelte';
    export let nodes:NodeList;
    const imageSrc = (i:Element) => {
        if (i.hasAttribute('remote')) {
            return i.getAttribute('remote')+"/"+i.getAttribute('source')
        } else {
            return i.getAttribute('source')
        }
    }
</script>

{#each nodes as node}
    {#if node.nodeType == Node.TEXT_NODE}
        {node.textContent}
    {:else if node instanceof Element}
        {#if node.nodeName.toLowerCase() == "m"}
            <Math latex={node.textContent} displayMode={node.getAttribute('mode')=="display"}/>
        {:else if node.nodeName.toLowerCase() == "me"}
            <Math latex={node.textContent} displayMode/>
        {:else if node.nodeName.toLowerCase() == "c"}
            <code>{node.textContent}</code>
        {:else if node.nodeName.toLowerCase() == "em"}
            <em><svelte:self nodes={node.childNodes}/></em>
        {:else if node.nodeName.toLowerCase() == "q"}
            "<svelte:self nodes={node.childNodes}/>"
        {:else if node.nodeName.toLowerCase() == "image"}
            <img style="max-width:100%" src={imageSrc(node)} alt={node.getAttribute('description')}/>
        {:else if node.nodeName.toLowerCase() == "url"}
            <a href={node.getAttribute("href")}>
                {#if node.textContent.trim()===''}
                    {node.getAttribute("href")}
                {:else}
                    <svelte:self nodes={node.childNodes}/>
                {/if}
            </a>
        {/if}
    {/if}
{/each}