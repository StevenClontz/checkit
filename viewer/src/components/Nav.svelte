<script lang="ts">
    import {
        Navbar,
        NavbarBrand,
        NavItem,
        NavLink,
        Nav,
        Input,
        FormGroup,
        Label,
        Collapse,
        NavbarToggler,
    } from 'sveltestrap';
    import {location} from 'svelte-spa-router';
    import { instructorEnabled } from '../stores/instructor';

    let isOpen = false;
    const handleUpdate = (event) => isOpen = event.detail.isOpen
    
    import {toggleCodeCell} from '../utils';
</script>

<Navbar color="primary" dark expand="md">
    <NavbarBrand href="https://checkit.clontz.org" target="_blank">☑️It</NavbarBrand>
    <NavbarToggler on:click={() => (isOpen = !isOpen)} />
    <Collapse {isOpen} navbar expand="md" on:update={handleUpdate}>
        <Nav navbar>
            <NavItem>
                <NavLink href="#/bank/">
                    Bank Home
                </NavLink>
            </NavItem>
            <NavItem>
                <NavLink on:click={toggleCodeCell}>
                    Code Cell
                </NavLink>
            </NavItem>
        </Nav>
        <Nav navbar class="ml-auto">
            <NavItem class="mr-1">
                <form class="form-inline">
                    <FormGroup check>
                    <Label check class="navbar-text">
                        <Input size="" readonly={false} type="checkbox" bind:checked={$instructorEnabled} />
                        Show instructor features
                    </Label>
                    </FormGroup>
                </form>
            </NavItem>
            {#if $instructorEnabled}
                <NavItem>
                    <NavLink href="#/assessment">
                        Assessment Builder
                    </NavLink>
                </NavItem>
            {/if}
        </Nav>
    </Collapse>
</Navbar>
