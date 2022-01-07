from IPython.display import display, Markdown, HTML
import ipywidgets as widgets
from os import listdir, path
from .bank import Bank
import io
from contextlib import redirect_stdout
from . import VERSION
from html import escape as escape_html

def run(bank=None):
    if bank is None:
        bank = Bank()
    menu_dropdown = widgets.Dropdown(
        options=[
            ('',''),
            ('Outcomes', 'outcome'),
            ('Bank', 'bank'),
        ],
        description='Menu:',
    )
    submenu = widgets.Output()
    menu_dropdown.observe(change_submenu(submenu,bank),names='value')
    display(Markdown(f"## {bank.title}"))
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
    description = widgets.Output()
    generated = widgets.Output()
    output = widgets.Output()

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
            preview = o.HTML_preview(pregenerated=False)
            output.clear_output()
            display(HTML(preview))

    def seed(*args):
        o = outcomes_dropdown.value
        output.clear_output()
        with output:
            display(Markdown(f"*Selecting pregenerated seed...*"))
            preview = o.HTML_preview(pregenerated=True)
            output.clear_output()
            display(HTML(preview))

    def build(*args):
        o = outcomes_dropdown.value
        output.clear_output()
        with output:
            display(Markdown("Generating 10,000 seeds..."))
            o.generate_exercises(regenerate=True)
        reset(only_generated=True)
        with output:
            display(Markdown("Done!"))

    outcomes_dropdown.observe(reset,names="value")
    preview_button.on_click(preview)
    seed_button.on_click(seed)
    build_button.on_click(build)

    display(widgets.HBox([outcomes_dropdown,preview_button,seed_button,build_button]))
    display(description)
    display(generated)
    display(output)
    reset()

def bank_submenu(bank): 
    options = [
        (f"{o.slug}: {o.title}",o) for o in bank.outcomes()
    ]
    outcomes_select = widgets.SelectMultiple(
        options=options,
        value=[o[1] for o in options],
        rows=min(6,len(options)),
        description='Outcomes:',
    )
    amount_input = widgets.BoundedIntText(
        value=300,
        min=1,
        max=1000,
        step=1,
        description='# Exercises:'
    )
    publicity_dropdown = widgets.Dropdown(options=[("Private",False),("Public",True)],
        description='Publicity:')
    build_label = widgets.Label(value="Build:")
    viewer_button = widgets.Button(description="Viewer")
    canvas_button = widgets.Button(description="Canvas")
    brightspace_button = widgets.Button(description="Brightspace")
    moodle_button = widgets.Button(description="Moodle")
    buttons = widgets.HBox([build_label,viewer_button,canvas_button,brightspace_button,moodle_button])
    output = widgets.Output()

    def viewer(*args):
        p = publicity_dropdown.value
        r = not p
        a = amount_input.value
        os = outcomes_select.value
        output.clear_output()
        with output:
            display(Markdown("Building Viewer..."))
            bank.write_json(public=p,amount=a,randomized=r,outcomes=os)
            display(Markdown("Done!"))

    def canvas(*args):
        p = publicity_dropdown.value
        r = not p
        a = amount_input.value
        os = outcomes_select.value
        output.clear_output()
        with output:
            display(Markdown("Building Canvas..."))
            bank.write_canvas_zip(public=p,amount=a,randomized=r,outcomes=os)
            display(Markdown("Done!"))

    viewer_button.on_click(viewer)
    canvas_button.on_click(canvas)

    display(outcomes_select)
    display(publicity_dropdown)
    display(amount_input)
    display(buttons)
    display(output)


    # 
    # bank_slugs = [f for f in listdir('banks') if not path.isfile(path.join('banks', f))]
    # bank_slugs.sort()
    # bank_dropdown_options = ['']+bank_slugs
    # bank_dropdown = widgets.Dropdown(options=bank_dropdown_options)
    # build_button = widgets.Button(description="Build bank files")
    # build_amount_widget = widgets.BoundedIntText(
    #     value=300,
    #     min=1,
    #     max=1000,
    #     step=1,
    #     description='Count:',
    # )
    # build_public_dropdown = widgets.Dropdown(options=[("Non-public",False),("Public",True)])

    # def bank_dropdown_callback(c=None):
    #     bank_output.clear_output()
    #     if bank_dropdown.value != bank_dropdown_options[0]:
    #         f = io.StringIO()
    #         with redirect_stdout(f):
    #             bank = Bank(bank_dropdown.value)
    #         bank_errors = f.getvalue()
    #         boilerplate_button = widgets.Button(description="Create missing outcome files",layout=widgets.Layout(width="auto"))
    #         def write_boilerplate(c=None):
    #             bank.write_outcomes_boilerplate()
    #             boilerplate_button.description = boilerplate_button.description + " - Done!"
    #         boilerplate_button.on_click(write_boilerplate)
    #         bank_suboutput = widgets.Output()
    #         def build_bank(c=None):
    #             bank_suboutput.clear_output()
    #             with bank_suboutput:
    #                 bank.generate_exercises(public=build_public_dropdown.value,amount=build_amount_widget.value,regenerate=True)
    #                 print("Now building all output formats...")
    #                 f = io.StringIO()
    #                 with redirect_stdout(f):
    #                     bank.build(public=build_public_dropdown.value,amount=build_amount_widget.value,regenerate=False)
    #                 display(Markdown(f.getvalue()))
    #         build_button.on_click(build_bank)
    #         outcomes_dropdown = widgets.Dropdown(options=[(f"{o.slug}: {o.title}",o) for o in bank.outcomes])
    #         def preview_outcome(c=None):
    #             bank_suboutput.clear_output()
    #             with bank_suboutput:
    #                 display(HTML(f"<strong>Description:</strong>" +
    #                              f"<em>{outcomes_dropdown.value.description}</em>"))
    #                 display(HTML(outcomes_dropdown.value.HTML_preview()))
    #         outcome_button = widgets.Button(description="Preview exercise")
    #         outcome_button.on_click(preview_outcome)
    #         with bank_output:
    #             display(Markdown(f'### {bank.title}'))
    #             display(HTML(bank_errors))
    #             display(boilerplate_button)
    #             display(widgets.HBox([build_button,build_public_dropdown,build_amount_widget]))
    #             display(widgets.HBox([outcome_button,outcomes_dropdown]))
    #             display(bank_suboutput)
    # bank_dropdown.observe(bank_dropdown_callback,names='value')

    # display(Markdown("### Select a bank directory"))
    # display(bank_dropdown)
    # display(bank_output)
