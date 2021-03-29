from IPython.display import display, Markdown
import ipywidgets as widgets
from os import listdir, path
from . import Bank

def run():
    bank_output = widgets.Output()
    bank_slugs = [f for f in listdir('banks') if not path.isfile(path.join('banks', f))]
    bank_slugs.sort()
    bank_dropdown_options = ['']+bank_slugs
    bank_dropdown = widgets.Dropdown(options=bank_dropdown_options)
    build_button = widgets.Button(description="Build bank files")
    build_amount_widget = widgets.BoundedIntText(
        value=300,
        min=1,
        max=1000,
        step=1,
        description='Count:',
    )
    build_public_dropdown = widgets.Dropdown(options=[("Non-public",False),("Public",True)])
    def bank_dropdown_callback(c=None):
        bank_output.clear_output()
        if bank_dropdown.value != bank_dropdown_options[0]:
            bank = Bank(bank_dropdown.value)
            bank_suboutput = widgets.Output()
            def build_bank(c=None):
                bank_suboutput.clear_output()
                with bank_suboutput:
                    bank.build(public=build_public_dropdown.value,amount=build_amount_widget.value)
            build_button.on_click(build_bank)
            outcomes_dropdown = widgets.Dropdown(options=[(f"{o.slug}: {o.title}",o) for o in bank.outcomes])
            def preview_outcome(c=None):
                bank_suboutput.clear_output()
                with bank_suboutput:
                    outcomes_dropdown.value.print_preview()
            outcome_button = widgets.Button(description="Preview exercise")
            outcome_button.on_click(preview_outcome)
            with bank_output:
                display(Markdown('### '+bank.title))
                display(widgets.HBox([build_button,build_public_dropdown,build_amount_widget]))
                display(widgets.HBox([outcome_button,outcomes_dropdown]))
                display(bank_suboutput)
    bank_dropdown.observe(bank_dropdown_callback,names='value')
    display(Markdown("### Select a bank directory"))
    display(bank_dropdown)
    display(bank_output)