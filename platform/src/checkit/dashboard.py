from IPython.display import display, Markdown, HTML
import ipywidgets as widgets
from os import listdir, path
from .bank import Bank
import io
from contextlib import redirect_stdout
from . import VERSION

BANK = Bank()

def run():
    menu_dropdown = widgets.Dropdown(
        options=[
            ('',''),
            ('Preview Outcome', 'outcome'),
        ],
        value='',
        description='Menu:',
    )
    submenu = widgets.Output()
    menu_dropdown.observe(change_submenu(submenu),names='value')

    display(Markdown(f"## {BANK.title}"))
    display(menu_dropdown)
    display(submenu)
    display(Markdown("---"))
    display(Markdown(f"`CheckIt Dashboard v{VERSION}`"))

def change_submenu(submenu):
    @submenu.capture(clear_output=True)
    def callback(value):
        if value['new'] == 'outcome':
            outcome_submenu()
    return callback

def outcome_submenu(): 
    options = [
        (f"{o.slug}: {o.title}",o) for o in BANK.outcomes
    ]
    outcomes_dropdown = widgets.Dropdown(options=options)
    outcome_button = widgets.Button(description="Generate preview")
    preview = widgets.Output()
    outcome_button.on_click(preview_outcome(preview,outcomes_dropdown.value))

    display(widgets.HBox([outcomes_dropdown,outcome_button]))
    display(preview)

def preview_outcome(preview,outcome):
    @preview.capture(clear_output=True)
    def callback(button):
        display(HTML(f"<strong>Description:</strong>" +
                    f"<em>{outcome.description}</em>"))
        display(HTML(outcome.HTML_preview()))
    return callback


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
