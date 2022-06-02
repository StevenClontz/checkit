<script lang="ts">
    import ParagraphNodes from '../NodeList/ParagraphNodes.svelte'
    export let paragraph:Element;
</script>

<p>
    <ParagraphNodes nodes={paragraph.childNodes}/>
</p>