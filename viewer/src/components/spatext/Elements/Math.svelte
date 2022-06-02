<script lang="ts">
    import katex from 'katex';
    export let latex:string;
    export let displayMode = false;
</script>

{@html katex.renderToString(latex,{throwOnError:false,displayMode:displayMode})}