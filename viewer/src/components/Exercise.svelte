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


    const modes = ['display', 'edit', 'html', 'embed', 'latex', 'pretext']
    const modeLabels = ['Display', 'Edit Template', 'HTML', 'Embed (HTML)', 'LaTeX', 'PreTeXt']
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

{#if embedded }
    <Knowl knowl={outcomeToStx(outcome,seed)}/>
{:else}
<Row>
    <Col sm={{ size: 10, offset: 1 }}>
        {#if mode == "display"}
            <Knowl knowl={outcomeToStx(outcome,seed)}/>
        {:else if mode == "edit"}
            <Row>
                <Col sm="6">
                    <textarea bind:value={outcome.template}/>
                </Col>
                <Col sm="6">
                    <Knowl knowl={outcomeToStx(outcome,seed)}/>
                </Col>
            </Row>
        {:else if mode == "html"}
            <textarea readonly value={outcomeToHtml(outcome,seed)}/>
        {:else if mode == "latex"}
            <textarea readonly value={outcomeToLatex(outcome,seed)}/>
        {:else if mode == "pretext"}
            <textarea readonly value={outcomeToPtx(outcome,seed)}/>
        {:else if mode == "embed"}
            <textarea readonly value={embed}/>
        {:else}
            Invalid mode.
        {/if}
    </Col>
</Row>
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