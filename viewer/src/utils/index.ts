import type {Bank, Assessment} from '../types';

import {isOpen as codeCellIsOpen} from '../stores/codecell';

import katex from 'katex';

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
            "tex": "",
            "exercises": [],
        }
        assessment.tex = assessmentPrefix
        slugs.forEach( (slug,i) => {
            let o = getOutcomeFromSlug(bank,slug)
            if (o) {
                let e = sample(o.exercises)
                assessment.tex = assessment.tex + "\n\n" + e.tex
                if (i%2===1) {
                    assessment.tex = assessment.tex + "\n\n\\newpage\n\n"
                }
                assessment.exercises = [...assessment.exercises, e]
            }
        })
        assessment.tex = assessment.tex + assessmentSuffix
        assessment.tex = assessment.tex.trim()
        return assessment
    }
