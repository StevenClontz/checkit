<script lang="ts">
    import {
        Navbar,
        NavbarBrand,
        NavItem,
        NavLink,
        Nav,
        Collapse,
        NavbarToggler,
    } from 'sveltestrap';
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
        <Nav navbar class="ms-auto">
            {#if $instructorEnabled}
                <NavItem class="d-none d-md-block">
                    <NavLink href="#/assessment">
                        Assessment Builder
                    </NavLink>
                </NavItem>
            {/if}
            <NavItem class="mr-1">
                <NavLink on:click={()=>$instructorEnabled=!$instructorEnabled}>
                    {#if $instructorEnabled}
                        🗹
                    {:else}
                        ☐
                    {/if}
                        Show instructor features
                </NavLink>
            </NavItem>
            {#if $instructorEnabled}
                <NavItem class="d-md-none">
                    <NavLink href="#/assessment">
                        Assessment Builder
                    </NavLink>
                </NavItem>
            {/if}
        </Nav>
    </Collapse>
</Navbar>
