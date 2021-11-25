<script lang="ts">
    import {
        Pagination, PaginationItem, PaginationLink
    } from 'sveltestrap';

    export let page: number;
    export let pages: number;
    export let label: string | undefined = undefined;
    export let keyboardControl: boolean = false;
    export let minimal: boolean = false;

    const pageRange = (p:number) => {
        let start = Math.max(0,Math.min(p-2,pages-5))
        let end = Math.min(pages,start+5)
        return Array.from({length: end-start}, (_, key) => start+key);
    }
    const setPage = (p:number) => (e:Event) => {
        e.preventDefault();
        page = p;
    }
    const handleKeydown = (e:KeyboardEvent) => {
        if (keyboardControl) {
            if (e.key === "ArrowLeft") {
                page = Math.max(0,page-1);
            } else if (e.key === "ArrowRight") {
                page = Math.min(pages-1,page+1);
            }
        }
    }
</script>


<svelte:window on:keydown={handleKeydown}/>

<div class="pagination">
    <Pagination ariaLabel={label}>
        {#if label}
        <PaginationItem disabled>
            <PaginationLink>{label}</PaginationLink>
        </PaginationItem>
        {/if}
        {#if !minimal}
        <PaginationItem disabled={page==0}>
            <PaginationLink first on:click={setPage(0)} />
        </PaginationItem>
        {/if}
        <PaginationItem disabled={page==0}>
            <PaginationLink previous on:click={setPage(page-1)} />
        </PaginationItem>
        {#each pageRange(page) as p}
            <PaginationItem active={page==p}>
                <PaginationLink on:click={setPage(p)}>{p+1}</PaginationLink>
            </PaginationItem>
        {/each}
        <PaginationItem disabled={page==pages-1}>
            <PaginationLink next on:click={setPage(page+1)} />
        </PaginationItem>
        {#if !minimal}
        <PaginationItem disabled={page==pages-1}>
            <PaginationLink last on:click={setPage(pages-1)} />
        </PaginationItem>
        {/if}
    </Pagination>
</div>

<style>
    .pagination {
        overflow-x: auto;
    }
</style>
