import { writable } from 'svelte/store';
import type { Bank } from '../types';

let _banks: Array<Bank> = [];

export const banks = writable(_banks);

let _bank: Bank;

export const bank = writable(_bank);