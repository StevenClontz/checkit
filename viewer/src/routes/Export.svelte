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

    const toManifest = (b:Bank) => {
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
    let working = false
    const zipUp = () => {
        working = true
        const zip = new JSZip()
        zip.file('imsmanifest.xml', toManifest($bank))
        $bank.outcomes.forEach((o)=>zip.file(`${o.slug}.xml`,toXml(o)))
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
            <Button on:click={zipUp} disabled={working} color="primary">
                {#if working}
                    Exporting...
                {:else}
                    Export to LMS
                {/if}
            </Button>
        </p>
    </Container>
</main>

<style>
    h1 { margin-top:0.5em }
</style>
