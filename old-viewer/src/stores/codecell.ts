import { writable } from 'svelte/store';

let _isOpen: Boolean = false;
export const isOpen = writable(_isOpen);