<script lang="ts">
    import {
        Container,
        Jumbotron,
    } from 'sveltestrap';
    import BankDropdown from './dropdowns/Bank.svelte';
</script>

<Jumbotron>
    <Container>
        <h1 class="display-3">☑️It</h1>
        <p class="lead">Free and open randomized exercises for practice and assessment.</p>

        <ul>
            <li>
                <span class="lead">For <strong>students</strong>:</span> Use these exercises to ✔️
                your understanding of your course's learning outcomes.
            </li>
            <li>
                <span class="lead">For <strong>instructors</strong>:</span> Use these exercises in
                assessments to help you ✔️ on student understanding.
            </li>
        </ul>

        <p class="lead">
            <BankDropdown/>
        </p>
    </Container>
</Jumbotron>