<script lang="ts">
    import ContentNodes from "../NodeList/ContentNodes.svelte"
    export let content:Element;
</script>

<ContentNodes nodes={content.childNodes} allowKnowls/>
