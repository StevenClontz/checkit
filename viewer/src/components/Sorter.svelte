<script lang="ts">
    import DragDropList from 'svelte-dragdroplist';

    export let array:Array<any>;

    export let removesItems = true;
    export let display = (element:any) => element;

    let ddArray = array.map((item,i)=>{
        return {
            'text': display(item),
            'item': item,
            'id': i,
        }
    });
    $: array = ddArray.map((i)=>i.item);
</script>

{#if array.length > 0}
    <DragDropList bind:data={ddArray} {removesItems}/>
{/if}
