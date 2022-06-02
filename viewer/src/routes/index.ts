import Home from './Home.svelte';
import Bank from './Bank.svelte';
import Export from './Export.svelte';
import Outcome from './Outcome.svelte';
import OutcomeRedirect from './OutcomeRedirect.svelte';
import NotFound from './NotFound.svelte';
import Assessment from './Assessment.svelte';

export const routes = {
    '/': Home,
    '/bank/': Bank,
    '/bank/:outcomeSlug/': OutcomeRedirect,
    '/bank/:outcomeSlug/:exerciseVersion/': Outcome,
    '/assessment/': Assessment,
    '/export/': Export,
    '*': NotFound,
}