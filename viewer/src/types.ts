export type Bank = {
    title: string;
    url: string;
    generated_on: string;
    outcomes: Array<Outcome>;
}
export type Outcome = {
    title: string;
    slug: string;
    description: string;
    template: string;
    exercises: Array<Exercise>;
}
export type Exercise = {
    seed: number;
    data: Object;
}
export type Params = {
    outcomeSlug: string;
    exerciseVersion: string;
}
export type Assessment = {
    exercises: Exercise[]
    tex: string
}