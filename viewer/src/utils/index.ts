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

const parser = new DOMParser()

export const outcomeToStx = (o:Outcome,seed:number) => {
    const stxString:string = Mustache.render(o.template, o.exercises[seed]['data'])
    if (parser.parseFromString(stxString, "application/xml").querySelector('parsererror')) {
        let knowl = document.createElement("knowl")
        knowl.insertAdjacentHTML("afterbegin","<content><p>Error parsing template.</p></content>")
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

export const outcomeToHtml = (o:Outcome,seed:number) => {
    const e = outcomeToStx(o,seed)
    const transform = new XSLTProcessor()
    const xslDom = parser.parseFromString(htmlXsl, "application/xml")
    transform.importStylesheet(xslDom)
    return transform.transformToDocument(e).querySelector("div.stx").outerHTML.trim()
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
    const assessmentPrefix = `
\\documentclass[11pt]{exam}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                        Edit settings                        %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\newcommand{\\assessmentTitle}{
CheckIt Assessment
}
\\newcommand{\\assessmentVersion}{
Version ${Date.now()}
}
\\newcommand{\\assessmentInstructions}{
Do not use any unapproved aids while taking this assessment.
Read each question carefully and be sure to show all work
in the space provided.
}
%\\printanswers % uncomment to show answers

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



\\usepackage{amsfonts,amssymb,amsmath,amsthm}
\\setcounter{MaxMatrixCols}{50}
\\usepackage{enumerate}
\\usepackage{graphicx}
\\usepackage{caption}
\\pagestyle{headandfoot}
\\firstpageheader{\\assessmentTitle \\hspace{2em} \\assessmentVersion}{}{Name: \\underline{\\hspace{2.5in}}\\\\ID: \\underline{\\hspace{2.5in}}}
\\runningheader{\\assessmentTitle}{}{Page \\thepage\\ of \\numpages}
\\runningheadrule
\\firstpagefooter{}{}{}
\\runningfooter{}{}{}
\\renewcommand{\\solutiontitle}{\\noindent\\textbf{Answer:}}
\\newenvironment{exercise}[3]{\\question}{\\vfill}
\\newenvironment{exerciseStatement}{}{}
\\newenvironment{exerciseAnswer}{\\begin{solution}}{\\end{solution}}

\\begin{document}

\\begin{center}
\\fbox{\\fbox{\\parbox{6in}{\\centering\\assessmentInstructions}}}
\\end{center}

\\begin{questions}

`
    const assessmentSuffix = `

\\end{questions}

\\end{document}
`
        let assessment: Assessment = {
            "latex": "",
            "exercises": [],
        }
        assessment.latex = assessmentPrefix
        slugs.forEach( (slug,i) => {
            let o = getOutcomeFromSlug(bank,slug)
            if (o) {
                let seed = Math.floor(Math.random() * o.exercises.length);
                let e = sample(o.exercises)
                assessment.latex = assessment.latex + "\n\n" + e.tex
                assessment.latex = assessment.latex + "\n\n\\newpage\n\n"
                assessment.exercises = [...assessment.exercises, {outcome:o,seed:seed}]
            }
        })
        assessment.latex = assessment.latex + assessmentSuffix
        assessment.latex = assessment.latex.trim()
        return assessment
    }
