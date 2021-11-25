<script lang="ts">
    import Pagination from '../components/Pagination.svelte';
    import Exercise from '../components/Exercise.svelte';
    import type { Params } from '../types';
    import { Button, Row, Col } from 'sveltestrap';
    import { bank } from '../stores/banks';
    import { instructorEnabled, assessmentOutcomeSlugs } from '../stores/instructor';
    import Bank from './Bank.svelte';
    import { push, querystring } from 'svelte-spa-router';
    import { toggleCodeCell } from '../utils';

    export let params:Params;

    const toggleAnswer = () => hiddenAnswer = !hiddenAnswer;
    const handleKeydown = (e:KeyboardEvent) => {
        if (e.key === " ") {
            toggleAnswer()
        }
    }
    const versionStringToInt = (vs:string) => parseInt(vs)-1

    $: outcome = $bank.outcomes.find((o)=>o.slug==params.outcomeSlug);
    $: version = versionStringToInt(params.exerciseVersion);
    $: exercise = outcome.exercises[version]
    $: pages = Math.min(20,outcome.exercises.length)
    let hiddenAnswer = true; 
    let page = versionStringToInt(params.exerciseVersion);
    let outcomeSlug = params.outcomeSlug;
    $: if (outcomeSlug !== params.outcomeSlug) {
        page = version;
        outcomeSlug = params.outcomeSlug;
    }
    $: if (page !== version) {
        push(`/bank/${params.outcomeSlug}/${page+1}/${$querystring ? "?"+$querystring : ""}`);
    }
    $: countInAssessment = $assessmentOutcomeSlugs.filter(slug=>slug==outcome.slug).length
    const addToAssessment = () => {
        $assessmentOutcomeSlugs = [...$assessmentOutcomeSlugs, outcome.slug]
    }
    const removeFromAssessment = () => {
        let i = $assessmentOutcomeSlugs
            .map(slug=>slug==outcome.slug)
            .lastIndexOf(true)
        $assessmentOutcomeSlugs = [
            ...$assessmentOutcomeSlugs.slice(0, i),
            ...$assessmentOutcomeSlugs.slice(i + 1)
        ]
    }
</script>

<svelte:window on:keydown={handleKeydown}/>

<Bank {params}>
    
    {#if $querystring=="embed"}<h5>{outcomeSlug} — {outcome.title}</h5>{/if}
    <p>
        {outcome.description}
    </p>
    
    {#if $querystring=="embed" }
        <p class="d-none d-sm-block">
            <Pagination
                label="Version:"
                keyboardControl
                bind:page={page}
                {pages}/>
        </p>
        <p class="d-block d-sm-none">
            <Pagination minimal bind:page={page} {pages}/>
        </p>
        <p>
            Show/Hide:
            <Button color="info" outline on:click={toggleAnswer}>
                Answer
            </Button>
            <Button color="secondary" outline on:click={toggleCodeCell}>
                Code Cell
            </Button>
        </p>
    {:else}
    <Row>
        <Col xs="auto">
            <p class="d-none d-sm-block">
                <Pagination
                    label="Version:"
                    keyboardControl
                    bind:page={page}
                    {pages}/>
            </p>
            <p class="d-block d-sm-none">
                <Pagination minimal bind:page={page} {pages}/>
            </p>
        </Col>
        <Col xs="auto">
            <p>
                Show/Hide:
                <Button color="info" outline on:click={toggleAnswer}>
                    Answer
                </Button>
                <Button color="secondary" outline on:click={toggleCodeCell}>
                    Code Cell
                </Button>
            </p>
        </Col>
        {#if $instructorEnabled }
            <Col xs="auto">
                <p>
                    <span># Included in Assessment:</span>
                    <span class="btn-group ml-2" role="group">
                        <Button
                            color="success" 
                            disabled={countInAssessment<1} 
                            on:click={removeFromAssessment}>
                            -
                        </Button>
                        <Button
                            color="success"
                            outline>
                            {countInAssessment}
                        </Button>
                        <Button
                            color="success" 
                            on:click={addToAssessment}>
                            +
                        </Button>
                    </span>
                </p>
            </Col>
        {/if}
    </Row>
    {/if}
    
    <div class='mt-2'>
        <Exercise {hiddenAnswer} {exercise} {outcome} {page} embedded={$querystring=="embed"}/>
    </div>
</Bank>
