<script lang="ts">
    import Exercise from '../components/Exercise.svelte';
    import type { Params } from '../types';
    import { Button, Row, Col } from 'sveltestrap';
    import { bank } from '../stores/banks';
    import { instructorEnabled, assessmentOutcomeSlugs } from '../stores/instructor';
    import Bank from './Bank.svelte';
    import { push, querystring } from 'svelte-spa-router';
    import { toggleCodeCell } from '../utils';

    export let params:Params;

    const versionStringToInt = (vs:string) => parseInt(vs)-1

    $: outcome = $bank.outcomes.find((o)=>o.slug==params.outcomeSlug);
    $: version = versionStringToInt(params.exerciseVersion);
    let seed = versionStringToInt(params.exerciseVersion);
    let outcomeSlug = params.outcomeSlug;
    $: if (outcomeSlug !== params.outcomeSlug) {
        seed = version;
        outcomeSlug = params.outcomeSlug;
    }
    $: if (seed !== version) {
        push(`/bank/${params.outcomeSlug}/${seed+1}/${$querystring ? "?"+$querystring : ""}`);
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

    const changeSeed = (diff:number) => {
        seed = Math.max(0,Math.min(19,seed+diff))
    }
</script>

<Bank {params}>
    
    {#if $querystring=="embed"}<h5>{outcomeSlug} — {outcome.title}</h5>{/if}
    <p>
        {outcome.description}
    </p>
    
    <Row>
        <Col xs="auto">
            <div class="input-group mb-3">
                <label class="input-group-text" for="versionSelect">Version</label>
                <button class="btn btn-dark" on:click={()=>changeSeed(-1)}>&laquo;</button>
                <select class="form-select" label="versionSelect" bind:value={seed}>
                    {#each Array(20) as _, i}
                        <option value={i}>
                            {i+1}
                        </option>
                    {/each}
                </select>
                <button class="btn btn-dark" on:click={()=>changeSeed(+1)}>&raquo;</button>
            </div>
        </Col>
        <Col xs="auto">
            <p>
                <Button color="secondary" outline on:click={toggleCodeCell}>
                    Show/Hide Code Cell
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
    
    <div class='mt-2'>
        <Exercise {outcome} {seed} embedded={$querystring=="embed"}/>
    </div>
</Bank>
