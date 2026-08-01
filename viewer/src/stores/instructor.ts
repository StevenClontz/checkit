import { writable } from 'svelte/store';
// @ts-ignore
import defaultAssessmentTemplateRaw from '../templates/assessmentTemplate.tex?raw'

export const defaultAssessmentTemplate = defaultAssessmentTemplateRaw;

let _ie = false;
if (localStorage.getItem(location.pathname+'#instructorEnabled')) {
    try {
        let _ietry = JSON.parse(localStorage.getItem(location.pathname+'#instructorEnabled'));
        if (typeof _ietry == 'boolean') { _ie = _ietry }
    } catch {}
}
export const instructorEnabled = writable(_ie);
instructorEnabled.subscribe(value => {
    localStorage.setItem(location.pathname+"#instructorEnabled", JSON.stringify(value));
});

let _ao: Array<string> = [];
if (localStorage.getItem(location.pathname+'#assessmentOutcomeSlugs')) {
    try {
        let _aotry = JSON.parse(localStorage.getItem(location.pathname+'#assessmentOutcomeSlugs'));
        if (Array.isArray(_aotry)) { _ao = _aotry }
    } catch {}
}
export const assessmentOutcomeSlugs = writable(_ao);
assessmentOutcomeSlugs.subscribe(value => {
    localStorage.setItem(location.pathname+"#assessmentOutcomeSlugs", JSON.stringify(value));
});

let _at: string = defaultAssessmentTemplate;
if (localStorage.getItem(location.pathname+'#assessmentTemplate')) {
    try {
        let _attry = JSON.parse(localStorage.getItem(location.pathname+'#assessmentTemplate'));
        if (typeof _attry == 'string') { _at = _attry }
    } catch {}
}
export const assessmentTemplate = writable(_at);
assessmentTemplate.subscribe(value => {
    localStorage.setItem(location.pathname+"#assessmentTemplate", JSON.stringify(value));
});
