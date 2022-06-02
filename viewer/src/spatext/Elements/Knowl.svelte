<script lang="ts">
    import Content from './KnowlContent.svelte';
    import Title from './Title.svelte'
    export let knowl:Element;
    let showOuttro = false;
    const toggleOuttro = (e:Event) => {
        e.preventDefault()
        showOuttro=!showOuttro
    }
    const isInExercise = (p:Element) => {
        if (p.getAttribute("mode")=="exercise") return true
        if (p.parentElement!=null && p.parentElement.tagName=="knowl") return isInExercise(p.parentElement)
        return false
    }
    let outtroLabel:string
    let partLabel:string
    let knowlLabel:string
    $: if (isInExercise(knowl)) {
        outtroLabel = "solution"
        partLabel = "Task"
        knowlLabel = "Exercise"
    } else {
        outtroLabel = "outtro"
        partLabel = "Part"
        knowlLabel = "Knowl"
    }
    $: isTopKnowl = (knowl.parentElement?.tagName!="knowl")
    const numbering = (p:Element) => {
        let parentPart = p.parentElement
        if (parentPart?.tagName!="knowl") {
            return ""
        } else {
            let base = numbering(parentPart)
            if (base!="") {
                base = base+"."
            }
            let siblings = [...parentPart.querySelectorAll("knowl")]
            return base + (siblings.indexOf(p)+1).toString()
        }
    }
    $: title = knowl.querySelector(":scope > title")
</script>

{#if numbering(knowl)!=""}
    <h5>{partLabel} {numbering(knowl)}.</h5>
{:else}
    <h3>
        {knowlLabel}{#if title}: <Title {title}/>{:else}.{/if}
    </h3>
{/if}
<div class:top-knowl={isTopKnowl}>
    {#if knowl.querySelector(":scope > intro")!=null}
        <Content content={knowl.querySelector("intro")}/>
    {/if}
    {#if knowl.querySelectorAll(":scope > content").length > 0}
        <Content content={knowl.querySelector(":scope > content")}/>
    {:else}
        <ol>
            {#each knowl.querySelectorAll(":scope > knowl") as subKnowl}
                <li class="sub-knowl">
                    <svelte:self knowl={subKnowl}/>
                </li>
            {/each}
        </ol>
    {/if}
    {#if knowl.querySelectorAll(":scope > outtro").length > 0}
        <div class="outtro">
            <p>
                <a class="toggle" href="#toggle" on:click={toggleOuttro}>
                    {#if showOuttro}
                        &blacktriangledown; Hide
                    {:else}
                        &blacktriangleright; Show
                    {/if}
                    {outtroLabel}
                </a>
            </p>
            {#if showOuttro}
                <Content content={knowl.querySelector(":scope > outtro")}/>
            {/if}
        </div>
    {/if}
</div>

<style>
    .toggle {
        color:rgb(100, 100, 100);
        font-size: 0.8em;
    }
    ol {
        list-style: none;
    }
    .outtro {
        border-color: rgb(90, 90, 90);
        border-width: 1px;
        border-radius: 5px;
        border-style: solid;
        padding: 0 1em;
        margin: 1em 0;
    }
    .top-knowl {
        border-color: rgb(0, 0, 0);
        border-width: 1px;
        border-radius: 5px;
        border-style: solid;
        padding: 0 1em;
        margin: 1em 0;
    }
</style>