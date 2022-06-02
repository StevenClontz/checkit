<script lang="ts">
    import type { Params, Outcome, Bank as BankType } from '../types';
    import { bank } from '../stores/banks';
    import Bank from './Bank.svelte';
    import Mustache from 'mustache';

    import {outcomeToHtml} from '../utils/index'

    // @ts-ignore
    import canvasManifest from '../templates/canvasManifest.xml?raw'
    // @ts-ignore
    import canvasOutcomeXml from '../templates/canvasOutcomeXml.xml?raw'


    export let params:Params;
    const toManifest = (b:BankType) => {
        return Mustache.render(canvasManifest, {
            "title": b.title,
            "id": Date.now(),
            "slugs": b.outcomes.map((o)=>{
                return {"slug":o.slug}
            })
        })
    }
    const toXmlContext = (o:Outcome) => {
        return {
            "slug": o.slug,
            "title": o.title,
            "question_type": "file_upload_question", //essay_question
            "exercises": Array.from(Array(20)).map((_, i) => {
                return {
                    "seed": i,
                    "generated_on": new Date(Date.now()).toISOString(),
                    "question": outcomeToHtml(o,i,true,"hide"),
                    "answer": outcomeToHtml(o,i,true,"only"),
                }
            })
        }
    }
    const toXml = (o:Outcome) => {
        return Mustache.render(canvasOutcomeXml, toXmlContext(o))
    }
</script>

<Bank {params}>
    <div>
        <textarea readonly value={toManifest($bank)}/>
    </div>
    {#each $bank.outcomes as o}
        <div>
            {o.slug}
            <textarea readonly value={toXml(o)}/>
        </div>
    {/each}
</Bank>

<style>
    textarea {
        width:100%;
        height:25em;
        font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace;
    }
    textarea[readonly] {
        background-color: #eee;
    }
</style>
