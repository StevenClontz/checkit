from IPython.display import display, Markdown, HTML
import ipywidgets as widgets
from .bank import Bank
from . import VERSION
from html import escape as escape_html

class modifiedOutput(widgets.Output):
    """
    https://github.com/jupyter-widgets/ipywidgets/issues/3208#issuecomment-1070836153
    """
    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)

def run(bank=None):
    if bank is None:
        bank = Bank()
    menu_dropdown = widgets.Dropdown(
        options=[
            ('',''),
            ('Author/edit outcomes', 'outcome'),
            ('Manage bank', 'bank'),
        ],
        description='Menu:',
    )
    submenu = widgets.Output()
    menu_dropdown.observe(change_submenu(submenu,bank),names='value')
    display(Markdown(f"## {bank.title}"))
    display(HTML("<style>.stx-outtro{background-color:#ddd;}</style>"))
    display(menu_dropdown)
    display(submenu)
    display(Markdown("---"))
    display(Markdown(f"`CheckIt Dashboard v{VERSION}`"))

def change_submenu(submenu,bank):
    @submenu.capture(clear_output=True)
    def callback(value):
        if value['new'] == 'outcome':
            outcome_submenu(bank)
        elif value['new'] == 'bank':
            bank_submenu(bank)
    return callback

def outcome_submenu(bank): 
    options = [
        (f"{o.slug}: {o.title}",o) for o in bank.outcomes()
    ]
    outcomes_dropdown = widgets.Dropdown(options=options,
        description='Outcome:')
    preview_button = widgets.Button(description="Fresh preview")
    seed_button = widgets.Button(description="View random seed")
    build_button = widgets.Button(description="Generate seeds")
    images_button = widgets.Button(description="Gen seeds+graphics")
    description = modifiedOutput()
    generated = modifiedOutput()
    output = modifiedOutput()

    def reset(*args,only_generated=False):
        o = outcomes_dropdown.value
        if not only_generated:
            description.clear_output()
            with description:
                display(Markdown(f"**Description:** {escape_html(o.description)}"))
            output.clear_output()
        generated.clear_output()
        with generated:
            display(Markdown(f"*Last generated on:* `{o.generated_on()}`"))

    def preview(*args):
        o = outcomes_dropdown.value
        output.clear_output()
        with output:
            display(Markdown(f"*Generating fresh preview...*"))
        with output:
            preview = o.html_preview(pregenerated=False)
        with output:
            output.clear_output()
            display(HTML(preview))

    def seed(*args):
        o = outcomes_dropdown.value
        output.clear_output()
        with output:
            display(Markdown(f"*Selecting pregenerated seed...*"))
        with output:
            preview = o.html_preview(pregenerated=True)
        with output:
            output.clear_output()
            display(HTML(preview))

    def build(*args):
        o = outcomes_dropdown.value
        output.clear_output()
        with output:
            display(Markdown("Generating 1,000 seeds..."))
        with output:
            o.generate_exercises(regenerate=True)
        reset(only_generated=True)
        with output:
            display(Markdown("Done!"))

    def images(*args):
        o = outcomes_dropdown.value
        output.clear_output()
        with output:
            display(Markdown("Generating 1,000 seeds with graphics... (this can take some time)"))
        with output:
            o.generate_exercises(regenerate=True,images=True)
        reset(only_generated=True)
        with output:
            display(Markdown("Done!"))

    outcomes_dropdown.observe(reset,names="value")
    preview_button.on_click(preview)
    seed_button.on_click(seed)
    build_button.on_click(build)
    images_button.on_click(images)

    display(outcomes_dropdown)
    display(widgets.HBox([preview_button,seed_button,build_button,images_button]))
    display(description)
    display(generated)
    display(output)
    reset()

def bank_submenu(bank):
    build_label = widgets.Label(value="Build:")
    json_button = widgets.Button(description="Bank from cache")
    json_regen_button = widgets.Button(description="Regenerated bank")
    buttons = widgets.HBox([build_label,json_button,json_regen_button])
    output = modifiedOutput()
    generated = modifiedOutput()

    def reset(*args):
        output.clear_output()
        with output:
            display(Markdown(f"*Last built on:* `{bank.generated_on()}`"))

    def json(*args):
        generated.clear_output()
        with generated:
            display(Markdown("Building bank from pregenerated outcomes..."))
        with generated:
            bank.write_json()
        with generated:
            bank.build_viewer()
        reset()
        with generated:
            display(Markdown("Done!"))

    def json_regen(*args):
        generated.clear_output()
        with generated:
            display(Markdown("Regenerating all outcomes (no graphics) and building bank..."))
        with generated:
            bank.write_json(regenerate=True)
        with generated:
            bank.build_viewer()
        reset()
        with generated:
            display(Markdown("Done!"))

    json_button.on_click(json)
    json_regen_button.on_click(json_regen)

    display(buttons)
    display(output)
    display(generated)
    reset()
