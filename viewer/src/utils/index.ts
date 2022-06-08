import type {Bank, Assessment, Outcome} from '../types';

import {isOpen as codeCellIsOpen} from '../stores/codecell';

import katex from 'katex';

import Mustache from 'mustache';
// @ts-ignore
import latexXsl from '../spatext/xsl/latex.xsl?raw'
// @ts-ignore
import htmlXsl from '../spatext/xsl/html.xsl?raw'
// @ts-ignore
import ptxXsl from '../spatext/xsl/pretext.xsl?raw'
// @ts-ignore
import assessmentTemplate from '../templates/assessmentTemplate.tex?raw'

const parser = new DOMParser()

export const outcomeToStx = (o:Outcome,seed:number) => {
    let stxString:string
    try {
        stxString = Mustache.render(o.template, o.exercises[seed]['data'])
    } catch (error) {
        stxString = "<knowl><content><p><em>ERROR:</em> Mustache template could not be parsed.</p></content></knowl>"
    }
    if (parser.parseFromString(stxString, "application/xml").querySelector('parsererror')) {
        let knowl = document.createElement("knowl")
        knowl.insertAdjacentHTML("afterbegin","<content><p><em>ERROR:</em> XML could not be parsed.</p></content>")
        return knowl
    }
    let stxElement = parser.parseFromString(stxString, "application/xml").querySelector(":scope")
    stxElement.querySelectorAll("image").forEach(image => {
        image.setAttribute("remote", `${location.protocol}//${location.host}${location.pathname}`)
    });
    return stxElement
}

export const outcomeToLatex = (o:Outcome,seed:number) => {
    const e = outcomeToStx(o,seed)
    const transform = new XSLTProcessor()
    const xslDom = parser.parseFromString(latexXsl, "application/xml")
    transform.importStylesheet(xslDom)
    return transform.transformToDocument(e).querySelector(":scope").textContent.trim()
}

export const outcomeToHtml = (o:Outcome,seed:number,canvasMath=false,solutions:'show'|'hide'|'only'='show') => {
    const e = outcomeToStx(o,seed)
    const transform = new XSLTProcessor()
    const xslDom = parser.parseFromString(htmlXsl, "application/xml")
    transform.importStylesheet(xslDom)
    let ele = transform.transformToDocument(e).querySelector("div.stx")
    if (canvasMath) {
        ele.querySelectorAll(".math[data-latex]").forEach((math)=>{
            const imageMath = document.createElement('img');
            imageMath.setAttribute(
                "src",
                `https://canvas.instructure.com/equation_images/${encodeURIComponent(encodeURIComponent(math.getAttribute("data-latex")))}`
            )
            imageMath.setAttribute(
                "alt",
                `LaTeX formula: ${math.getAttribute("data-latex")}`
            )
            imageMath.setAttribute(
                "title",
                `LaTeX formula: ${math.getAttribute("data-latex")}`
            )
            imageMath.style.padding = "5px"
            imageMath.style.border = "solid 1px #ddd"
            imageMath.style.borderRadius = "5px"
            math.parentElement.replaceChild(imageMath,math)
        })
    }
    if (solutions=="hide") {
        ele.querySelectorAll('.stx-outtro').forEach((outtro)=>{
            outtro.parentElement.removeChild(outtro)
        })
    }
    if (solutions=="only") {
        ele.querySelectorAll('.stx-intro').forEach((intro)=>{
            intro.parentElement.removeChild(intro)
        })
        ele.querySelectorAll('.stx-content').forEach((content)=>{
            content.parentElement.removeChild(content)
        })
    }
    return ele.outerHTML.trim()
}

export const outcomeToPtx = (o:Outcome,seed:number) => {
    const e = outcomeToStx(o,seed)
    const transform = new XSLTProcessor()
    const xslDom = parser.parseFromString(ptxXsl, "application/xml")
    transform.importStylesheet(xslDom)
    return transform.transformToDocument(e).querySelector(':scope').outerHTML.trim()
}

export const toggleCodeCell = () => {codeCellIsOpen.update(x=>!x)}

export const getOutcomeFromSlug = (bank:Bank,slug:string) =>
    bank.outcomes.find((o)=>o.slug===slug)

export const sample = (a:Array<any>) => a[Math.floor(Math.random()*a.length)]

export const decodeXmlString = (s:string) => {
    return s.replace(/&apos;/g, "'")
            .replace(/&quot;/g, '"')
            .replace(/&gt;/g, '>')
            .replace(/&lt;/g, '<')
            .replace(/&amp;/g, '&');
}

export const parseMath = (html:string) => {
    let inlineMathRe = /\\\((.*?)\\\)/gs;
    let displayMathRe = /\\\[(.*?)\\\]/gs;
    return html.replace(
        inlineMathRe,
        (_, tex:string) => katex.renderToString(decodeXmlString(tex), {
            'displayMode': false,
            'throwOnError': false,
        })
    ).replace(
        displayMathRe,
        (_, tex:string) => katex.renderToString(decodeXmlString(tex), {
            'displayMode': true,
            'throwOnError': false,
        })
    );
}

export const getRandomAssessmentFromSlugs = (bank:Bank,slugs:string[]) => {
    let assessment: Assessment = {
        "latex": "",
        "exercises": [],
    }
    slugs.forEach( (slug) => {
        let o = getOutcomeFromSlug(bank,slug)
        if (o) {
            // pull random seed besides first public 20
            let seed = Math.floor(Math.random() * (o.exercises.length-20))+20;
            assessment.latex = assessment.latex + "\n\n" + outcomeToLatex(o,seed)
            assessment.latex = assessment.latex + "\n\n\\newpage\n\n"
            assessment.exercises = [...assessment.exercises, {outcome:o,seed:seed}]
        }
    })
    assessment.latex = Mustache.render(
        assessmentTemplate, 
        {
            "version": Date.now(),
            "exercises": assessment.exercises.map((e)=>{
                return {"latex": outcomeToLatex(e.outcome,e.seed)}
            })
        }
    )
    return assessment
}
