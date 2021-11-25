<script lang="ts">
    import type { Params } from '../types';
	export let params:Params;
	import {push, querystring} from 'svelte-spa-router'
    push(`/bank/${params.outcomeSlug}/1/${$querystring ? "?"+$querystring : ""}`);
</script>