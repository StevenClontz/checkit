<script lang="ts">
    import type { Outcome } from '../types';
    import {
        Container,
        Row,
        Col,
        Button,
        FormGroup, Label, Input
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
            "exercises": Array.from(Array(900)).map((_, i) => {
                return {
                    "seed": i+100,
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
        // hax to update DOM before locking browser for build
        setTimeout(()=>{
            const zip = new JSZip()
            zip.file('imsmanifest.xml', toManifest())
            $bank.outcomes.forEach((o)=>zip.file(`${o.slug}.xml`, toXml(o)))
            zip.generateAsync({ type: 'blob' }).then(function (content) {
                working=false
                FileSaver.saveAs(content, 'canvasBank.zip')
            })
        },50)
    }
</script>

<main>
    <Container>
        <Row>
            <Col>
                <h1 class="display-4">☑️It Export to LMS</h1>
            </Col>
        </Row>
        <Row>
            <Col>
                <FormGroup>
                    <Label>Customize bank title</Label>
                    <Input type="text" bind:value={$bank.title} />
                </FormGroup>
            </Col>
        </Row>
        <Row>
            <Col>
                <h3>Canvas <small>(Question Banks / Classic Quizzes)</small></h3>
            </Col>
        </Row>
        <Row>
            <Col>
                <select class="form-select" label="versionSelect" bind:value={questionType}>
                    <option value="essay">
                        Essay response
                    </option>
                    <option value="upload">
                        File upload
                    </option>
                </select>
            </Col>
            <Col>
                <Button on:click={zipUp} disabled={working} color="primary">
                    {#if working}
                        Exporting...
                    {:else}
                        Export to Canvas
                    {/if}
                </Button>
            </Col>
        </Row>
    </Container>
</main>

<style>
    h1 { margin-top:0.5em }
</style>
