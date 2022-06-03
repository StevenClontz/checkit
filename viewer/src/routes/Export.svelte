<script lang="ts">
    import type { Outcome, Bank } from '../types';
    import {
        Container,
        Button,
    } from 'sveltestrap';
    import JSZip from 'jszip';
    import FileSaver from 'file-saver';
    import { bank } from '../stores/banks';
    import Mustache from 'mustache';

    import {outcomeToHtml} from '../utils/index'

    // @ts-ignore
    import canvasManifest from '../templates/canvasManifest.xml?raw'
    // @ts-ignore
    import canvasOutcomeXml from '../templates/canvasOutcomeXml.xml?raw'

    let id:number

    let questionType:"essay"|"upload"="upload"

    const toManifest = () => {
        return Mustache.render(canvasManifest, {
            "title": $bank.title,
            "id": id,
            "slugs": $bank.outcomes.map((o)=>{
                return {"slug":o.slug}
            })
        })
    }
    const toXmlContext = (o:Outcome) => {
        let ctx = {
            "slug": o.slug,
            "bank": $bank.title,
            "title": o.title,
            "id": id,
            questionType: true,
            "exercises": Array.from(Array(50)).map((_, i) => {
                return {
                    "seed": i+50,
                    "generated_on": new Date(Date.now()).toISOString(),
                    "question": outcomeToHtml(o,i,true,"hide"),
                    "answer": outcomeToHtml(o,i,true,"only"),
                }
            })
        }
        ctx[questionType] = true
        return ctx
    }
    const toXml = (o:Outcome) => {
        return Mustache.render(canvasOutcomeXml, toXmlContext(o))
    }
    let working = false
    function zipUp() {
        id = Date.now()
        working = true
        const zip = new JSZip()
        zip.file('imsmanifest.xml', toManifest())
        $bank.outcomes.forEach((o)=>zip.file(`${o.slug}.xml`, toXml(o)))
        zip.generateAsync({ type: 'blob' }).then(function (content) {
            working=false
            FileSaver.saveAs(content, 'canvasBank.zip')
        });
    }
</script>

<main>
    <Container>
        <h1 class="display-4">☑️It Export to LMS</h1>
        <p>
            <select class="form-select" label="versionSelect" bind:value={questionType}>
                <option value="essay">
                    Essay response
                </option>
                <option value="upload">
                    File upload
                </option>
            </select>
            <Button on:click={zipUp} disabled={working} color="primary">
                {#if working}
                    Exporting...
                {:else}
                    Export to Canvas
                {/if}
            </Button>
        </p>
    </Container>
</main>

<style>
    h1 { margin-top:0.5em }
</style>
