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
    import canvasOutcome from '../templates/canvasOutcome.xml?raw'
    // @ts-ignore
    import brightspaceManifest from '../templates/brightspaceManifest.xml?raw'
    // @ts-ignore
    import brightspaceBank from '../templates/brightspaceBank.xml?raw'
    // @ts-ignore
    import moodleBank from '../templates/moodleBank.xml?raw'

    let id:number

    let selectedOutcomeSlugs:Array<string> = []

    let questionType:"essay"|"upload"|"boolean"="upload"

    let lms:"canvas"|"brightspace"|"moodle"="canvas"

    const toCanvasManifest = () => {
        return Mustache.render(canvasManifest, {
            "title": $bank.title,
            "id": id,
            "slugs": selectedOutcomeSlugs.map((s)=>{
                return {"slug":s}
            })
        })
    }
    const toCanvasOutcomeContext = (o:Outcome) => {
        let ctx = {
            "slug": o.slug,
            "bank": $bank.title,
            "bankSlug": $bank.slug,
            "title": o.title,
            "questionType": questionType,
            "id": id,
            "exercises": Array.from(Array(900)).map((_, i) => {
                let seed=i+100
                return {
                    "seed": seed,
                    "generated_on": new Date(Date.now()).toISOString(),
                    "question": outcomeToHtml(o,seed,"canvas","hide"),
                    "answer": outcomeToHtml(o,seed,"canvas","only"),
                }
            })
        }
        ctx[questionType] = true
        return ctx
    }
    const toCanvasOutcome = (s:string) => {
        const o = $bank.outcomes.find((o)=>o.slug==s)
        return Mustache.render(canvasOutcome, toCanvasOutcomeContext(o))
    }
    const toBrightspaceManifest = () => {
        return Mustache.render(brightspaceManifest, {
            "title": $bank.title,
            "id": id,
            "slugs": selectedOutcomeSlugs.map((s)=>{
                return {"slug":s}
            })
        })
    }
    const toBrightspaceBank = () => {
        let ctx = {
            "id": id,
            "bank": $bank.title,
            "bankSlug": $bank.slug,
            questionType: true,
            "outcomes": selectedOutcomeSlugs.map(s => {
                let o = $bank.outcomes.find(o => o.slug == s)
                return {
                    "slug": o.slug,
                    "title": o.title,
                    "exercises": Array.from(Array(900)).map((_, i) => {
                        let seed = i+100
                        return {
                            "seed": seed,
                            "generated_on": new Date(Date.now()).toISOString(),
                            "question": outcomeToHtml(o,seed,"default","hide"),
                            "answer": outcomeToHtml(o,seed,"default","only"),
                        }
                    })
                }
            })
        }
        return Mustache.render(brightspaceBank, ctx)
    }
    const toMoodle = () => {
        let ctx = {
            "id": id,
            "bank": $bank.title,
            "bankSlug": $bank.slug,
            questionType: true,
            "outcomes": selectedOutcomeSlugs.map(s => {
                let o = $bank.outcomes.find(o => o.slug == s)
                return {
                    "slug": o.slug,
                    "title": o.title,
                    "exercises": Array.from(Array(900)).map((_, i) => {
                        let seed=i+100
                        return {
                            "seed": i+100,
                            "generated_on": new Date(Date.now()).toISOString(),
                            "question": outcomeToHtml(o,seed,"default","hide"),
                            "answer": outcomeToHtml(o,seed,"default","only"),
                        }
                    })
                }
            })
        }
        return Mustache.render(moodleBank, ctx)
    }
    let working = false
    function exportToLms() {
        id = Date.now()
        working = true
        // hax to update DOM before locking browser for build
        setTimeout(()=>{
            if (lms=="canvas") {
                const zip = new JSZip()
                zip.file('imsmanifest.xml', toCanvasManifest())
                selectedOutcomeSlugs.forEach((s)=>zip.file(`${s}.xml`, toCanvasOutcome(s)))
                zip.generateAsync({ type: 'blob' }).then(function (content) {
                    working=false
                    FileSaver.saveAs(content, 'canvasBank.zip')
                })
            } else if (lms=="brightspace") {
                const zip = new JSZip()
                zip.file('imsmanifest.xml', toBrightspaceManifest())
                zip.file('questiondb.xml', toBrightspaceBank())
                zip.generateAsync({ type: 'blob' }).then(function (content) {
                    working=false
                    FileSaver.saveAs(content, 'brightspaceBank.zip')
                })
            } else if (lms=="moodle") {
                let renderedBank = toMoodle()
                let blob = new Blob([renderedBank], {type: "text/plain;charset=utf-8"});
                FileSaver.saveAs(blob, 'moodleBank.xml')
                working=false
            }
        },50)
    }
</script>

<main>
    <Container>
        <Row>
            <Col>
                <h1 class="display-4">☑️It Export to LMS</h1>
                <div class="alert alert-warning">
LMS Export works best in Chrome. Exporting several outcomes at once may
lock up your browser or cause the build to fail, so exporting a few
outcomes at a time is advised.
                </div>
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
                <div class="mb-3">
                <FormGroup>
                    <Label>Select outcomes to export</Label>
                    <select class="form-select" multiple aria-label="multiple select outcomes" bind:value={selectedOutcomeSlugs}>
                        {#each $bank.outcomes as o}
                            <option value={o.slug}>{o.slug}: {o.title}</option>
                        {/each}
                    </select>
                </FormGroup>
                <!-- <Button size='sm' color="info" on:click={()=>selectedOutcomeSlugs=$bank.outcomes.map((o)=>o.slug)}>
                    Select all outcomes
                </Button>
                <Button size='sm' outline color="warning" on:click={()=>selectedOutcomeSlugs=[]}>
                    Unselect all outcomes
                </Button> -->
                </div>
            </Col>
        </Row>
        <Row>
            <Col>
                <select class="form-select" label="lmsSelect" bind:value={lms}>
                    <option value="canvas">
                        Canvas (New & Classic Quizzes)
                    </option>
                    <option value="brightspace">
                        D2L Brightspace
                    </option>
                    <option value="moodle">
                        Moodle
                    </option>
                </select>
            </Col>
            {#if lms=='canvas'}
                <Col>
                    <select class="form-select" label="versionSelect" bind:value={questionType}>
                        <option value="essay">
                            Essay response
                        </option>
                        <option value="upload">
                            File upload
                        </option>
                        <option value="boolean">
                            True/false (for feedback support in New Quizzes)
                        </option>
                    </select>
                </Col>
            {/if}
            <Col>
                <Button block on:click={exportToLms} disabled={working || selectedOutcomeSlugs.length == 0} color="primary">
                    {#if working}
                        Exporting...
                    {:else}
                        Export
                    {/if}
                </Button>
            </Col>
        </Row>
    </Container>
</main>

<style>
    h1 { margin-top:0.5em }
    select[multiple] { resize:vertical }
</style>
