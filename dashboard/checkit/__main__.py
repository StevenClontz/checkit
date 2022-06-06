import click
import os
from . import static, VERSION

@click.command()
@click.argument('directory', default='new-checkit-bank')
def main(directory):
    """
    Generates boilerplate for using the CheckIt Dashboard
    to author a new bank.
    """
    # create directories
    try:
        os.makedirs(directory)
    except FileExistsError:
        print(f"Error creating new bank: directory `{directory}` already exists")
        return
    # copy sample outcome template/generator
    example_outcome_dir = os.path.join(directory,'outcomes','EX1')
    os.makedirs(example_outcome_dir)
    for filename in ["template.xml","generator.sage"]:
        with open(os.path.join(example_outcome_dir,filename),"w") as f:
            f.write(static.read_resource(filename))
    # copy dashboard notebook and bank manifest
    for filename in ["dashboard.ipynb","bank.xml"]:
        with open(os.path.join(directory,filename),"w") as f:
            f.write(static.read_resource(filename))
    # copy gitignore
    with open(os.path.join(directory,".gitignore"),"w") as f:
        f.write(static.read_resource("gitignore.txt"))
    # generate requirements.txt
    with open(os.path.join(directory,"requirements.txt"),"w") as f:
        f.write(f"checkit-dashboard == {VERSION}")
    print(f"Successfully created new CheckIt bank in `{directory}`")

if __name__ == "__main__":
    main()