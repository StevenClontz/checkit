import { writable } from 'svelte/store';

let _ie = false;
if (localStorage.getItem('instructorEnabled')) {
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
if (localStorage.getItem('assessmentOutcomeSlugs')) {
    try {
        let _aotry = JSON.parse(localStorage.getItem(location.pathname+'#assessmentOutcomeSlugs'));
        if (Array.isArray(_aotry)) { _ao = _aotry }
    } catch {}
}
export const assessmentOutcomeSlugs = writable(_ao);
assessmentOutcomeSlugs.subscribe(value => {
    localStorage.setItem(location.pathname+"#assessmentOutcomeSlugs", JSON.stringify(value));
});