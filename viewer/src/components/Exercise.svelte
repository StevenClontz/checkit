<script lang="ts">
    import { afterUpdate } from 'svelte';
    import type { Exercise, Outcome } from '../types';
    import { instructorEnabled } from '../stores/instructor';
    import { Nav, NavItem, NavLink, Row, Col } from 'sveltestrap';
    import { parseMath, outcomeToStx } from '../utils';
    import Knowl from './spatext/Elements/Knowl.svelte';

    export let embedded:Boolean = false;

    export let outcome: Outcome;
    // export let exercise: Exercise;
    export let page = 0;
    export let statementOnly: boolean=false;


    const modes = ['display', 'edit', 'html', 'embed', 'tex', 'pretext']
    const modeLabels = ['Display', 'Edit Template', 'HTML', 'Embed (HTML)', 'LaTeX', 'PreTeXt']
    let mode = "display";
    const changeMode = (m:string) => (e:Event) => {
        e.preventDefault();
        mode = m;
    }
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
    {:else}
        <hr/>
    {/if}
{/if}

{#if embedded }
    <Knowl knowl={outcomeToStx(outcome,page)}/>
{:else}
<Row>
    <Col sm={{ size: 10, offset: 1 }}>
        {#if mode == "display"}
            <Knowl knowl={outcomeToStx(outcome,page)}/>
        {:else if mode == "edit"}
            <Row>
                <Col sm="6">
                    <textarea style="width:100%;height:20em" bind:value={outcome.template}/>
                </Col>
                <Col sm="6">
                    <Knowl knowl={outcomeToStx(outcome,page)}/>
                </Col>
            </Row>
        {:else if mode == "html"}
            <pre class="pre-scrollable"><code>html</code></pre>
        {:else if mode == "tex"}
            <pre class="pre-scrollable"><code>tex</code></pre>
        {:else if mode == "pretext"}
            <pre class="pre-scrollable"><code>pretext</code></pre>
        {:else if mode == "embed"}
            <pre class="pre-scrollable"><code>&lt;iframe title="Iframe CheckIt Outcome"
    width="800"
    height="450"
    src="{location.protocol}//{location.host}{location.pathname}#/bank/{outcome.slug}/{page+1}/?embed"&gt;
&lt;/iframe&gt;</code></pre>
        {:else}
            Invalid mode.
        {/if}
    </Col>
</Row>
{/if}

<style>
    pre {
        border: 1px #ddd solid;
        background-color: #eee;
        padding: 4px;
        border-radius: 5px;
    }
    .navtabs {
        margin-bottom: 1em;
    }
</style>