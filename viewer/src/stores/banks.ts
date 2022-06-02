import { writable } from 'svelte/store';
import type { Bank } from '../types';

let _bank: Bank;

export const bank = writable(_bank);