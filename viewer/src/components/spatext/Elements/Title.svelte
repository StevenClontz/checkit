<script lang="ts">
    import TitleNodes from "./../NodeList/TitleNodes.svelte"
    export let title:Element
</script>

<TitleNodes nodes={title.childNodes}/>
