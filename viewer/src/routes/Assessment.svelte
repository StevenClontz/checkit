<script lang="ts">
    import {
        Container,
        Row,
        Col,
        Button,
        ButtonDropdown,
        DropdownToggle,
        DropdownMenu,
        DropdownItem,
    } from 'sveltestrap';
    import OutcomeDropdown from '../components/dropdowns/Outcome.svelte';
    import Sorter from '../components/Sorter.svelte';
    import { assessmentOutcomeSlugs, instructorEnabled } from '../stores/instructor';
    import { bank } from '../stores/banks';
    import { getOutcomeFromSlug, getRandomAssessmentFromSlugs } from '../utils';
    import type { Assessment } from '../types';
    import Exercise from '../components/Exercise.svelte'

    $instructorEnabled = true
    $assessmentOutcomeSlugs = $assessmentOutcomeSlugs.filter(s=>getOutcomeFromSlug($bank,s)!==undefined)
    const display = (slug:string) => {
        let o = getOutcomeFromSlug($bank,slug);
        return `${slug} — ${o.title}`
    };
    let generatedAssessment: Assessment | undefined = undefined
    const generate = () => generatedAssessment = getRandomAssessmentFromSlugs($bank,$assessmentOutcomeSlugs)

    const copyToClipboard = (text:string) => () => {
        navigator.clipboard.writeText(text)
        alert("Copied to clipboard!")
    }
    let latexForm: HTMLFormElement
    const openInOverleaf = () => {
        latexForm.target = "_blank"
        latexForm.action = "https://www.overleaf.com/docs"
        latexForm.method = "POST"
        latexForm.submit()
    }
</script>

<main>
    <Container>
        <h1 class="display-4">☑️It Assessment Builder</h1>
        <Row>
            <Col sm="4">
                <p>
                    Build your assessment by first adding learning outcomes:
                </p>
                <p><OutcomeDropdown/></p>
                <p>
                    Then you can sort these outcomes into whatever order 
                    you wish. 
                </p>
            </Col>
            <Col sm="8">
                <div class="outcome-ordering">
                    {#if $assessmentOutcomeSlugs.length < 1}
                        (Add outcomes for your assessment.)
                    {/if}
                    <Sorter bind:array={$assessmentOutcomeSlugs} {display} removesItems/>
                    {#if $assessmentOutcomeSlugs.length > 0}
                        <a 
                            href="#."
                            on:click|preventDefault={()=>$assessmentOutcomeSlugs=[]}>
                            [Reset outcomes]
                        </a>
                    {/if}
                </div>
            </Col>
        </Row>
        <Row>
            <Col>
                <p>
                    Clicking "Generate" will choose a random exercise assessing
                    each outcome.
                </p>
                {#if generatedAssessment}
                    <form bind:this={latexForm}>
                        <p>
                            <em>Source code:</em>
                            <textarea
                                name="snip"
                                class="form-control text-monospace"
                                rows="4"
                                readonly
                                value={generatedAssessment.latex}
                            />
                        </p>
                    </form>
                {/if}
                <Row class="mb-2">
                    <Col xs="auto" class="ml-auto">
                        <Button
                            color="primary"
                            disabled={$assessmentOutcomeSlugs.length < 1}
                            outline={generatedAssessment !== undefined}
                            on:click={generate}>
                            {#if generatedAssessment}
                                Re-generate
                                {:else}
                                Generate
                            {/if}
                        </Button>
                    </Col>  
                    <Col xs="auto" class="mr-auto">
                        {#if generatedAssessment}
                            <ButtonDropdown>
                                <DropdownToggle caret>
                                    Export:
                                </DropdownToggle>
                                <DropdownMenu>
                                    <DropdownItem on:click={openInOverleaf}>
                                        Open PDF using Overleaf.com
                                    </DropdownItem>
                                    <DropdownItem
                                        on:click={copyToClipboard(generatedAssessment.latex)}>
                                        Copy LaTeX to your clipboard 📋
                                    </DropdownItem>
                                </DropdownMenu>
                            </ButtonDropdown>
                        {/if}
                    </Col>
                </Row>
                {#if generatedAssessment}
                    <h3>Preview</h3>
                    {#each generatedAssessment.exercises as exercise,i}
                        <h4>Exercise {i+1}</h4>
                        <Exercise outcome={exercise.outcome} seed={exercise.seed} statementOnly/>
                    {/each}
                {/if}
            </Col>
        </Row>
    </Container>
</main>

<style>
    h1 { margin-top:0.5em }
    .outcome-ordering {
        border: 1px #888 solid; 
        border-radius: 5px; 
        padding: 10px; 
        margin-bottom: 1em;
        color: gray;
        text-align: center;
    }
</style>