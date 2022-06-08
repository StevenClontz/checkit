<script lang="ts">
    import type { Outcome } from '../types';
    import { instructorEnabled } from '../stores/instructor';
    import { Nav, NavItem, NavLink, Row, Col } from 'sveltestrap';
    import { outcomeToStx, outcomeToHtml, outcomeToLatex, outcomeToPtx } from '../utils';
    import Knowl from '../spatext/Elements/Knowl.svelte';

    export let embedded:Boolean = false;

    export let outcome: Outcome;
    export let seed = 0;
    export let statementOnly: boolean=false;


    const modes = ['display', 'edit', 'embed', 'html', 'latex', 'pretext']
    const modeLabels = ['Display', 'Edit Template', 'Embed HTML', 'Raw HTML', 'LaTeX', 'PreTeXt']
    let mode = "display";
    const changeMode = (m:string) => (e:Event) => {
        e.preventDefault();
        mode = m;
    }
    let embed:string
    $: embed = `<iframe title="Iframe CheckIt Outcome"
    width="800"
    height="450"
    src="${location.protocol}//${location.host}${location.pathname}#/bank/${outcome.slug}/${seed+1}/?embed">
</iframe>`

    // let canvasMath = false
    // let canvasSolutions:'show'|'hide'|'only' = 'show'
</script>

{#if !statementOnly && !embedded}
    {#if $instructorEnabled}
        <div class="navtabs">
            <Nav tabs>
                {#each modes as m,i}
                    <NavItem>
                        <NavLink 
                            active={mode==m} 
                            on:click={changeMode(m)} 
                            href="#/">
                            {modeLabels[i]}
                        </NavLink>
                    </NavItem>
                {/each}
            </Nav>
        </div>
    {/if}
{/if}

{#if embedded || mode == "display"}
    <Knowl knowl={outcomeToStx(outcome,seed)}/>
{:else if mode == "edit"}
    <Row>
        <Col sm="6">
            <p><textarea bind:value={outcome.template}/></p>
            <p><textarea readonly value={JSON.stringify(outcome.exercises[seed]['data'], null, 2)}/></p>
        </Col>
        <Col sm="6">
            <Knowl knowl={outcomeToStx(outcome,seed)}/>
        </Col>
    </Row>
{:else if mode == "html"}
    <textarea readonly value={outcomeToHtml(outcome,seed)}/>
    <!-- <input type="checkbox" bind:checked={canvasMath}/>
    <select bind:value={canvasSolutions}>
        {#each ['show','hide','only'] as opt}
            <option value={opt}>{opt}</option>
        {/each}
    </select>
    {@html outcomeToHtml(outcome,seed,canvasMath,canvasSolutions)} -->
{:else if mode == "latex"}
    <textarea readonly value={outcomeToLatex(outcome,seed)}/>
{:else if mode == "pretext"}
    <textarea readonly value={outcomeToPtx(outcome,seed)}/>
{:else if mode == "embed"}
    <textarea readonly value={embed}/>
{:else}
    Invalid mode.
{/if}

<style>
    .navtabs {
        margin-bottom: 1em;
    }
    textarea {
        width:100%;
        height:25em;
        font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace;
    }
    textarea[readonly] {
        background-color: #eee;
    }
</style>