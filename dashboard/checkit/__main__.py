import click
from trogon import tui
import os
from . import static, VERSION, bank

@tui()
@click.group(
    short_help="CheckIt command line interface",)
def main():
    pass

# checkit new
@main.command(
    short_help="Generates boilerplate for using the CheckIt Dashboard to author a new bank.",
)
@click.argument('directory', default='new-checkit-bank')
def new(directory):
    """
    Generates boilerplate for using the CheckIt Dashboard
    to author a new bank.
    """
    # create directories
    try:
        os.makedirs(directory)
    except FileExistsError:
        print(f"Warning: directory `{directory}` already exists")
    # copy sample outcome template/generator
    example_outcome_dir = os.path.join(directory,'outcomes','EX1')
    os.makedirs(example_outcome_dir, exist_ok=True)
    for filename in ["template.xml","generator.sage"]:
        with open(os.path.join(example_outcome_dir,filename),"w") as f:
            f.write(static.read_resource(filename))
    # copy devcontainer stuff
    devcontainer_dir = os.path.join(directory, ".devcontainer")
    os.makedirs(devcontainer_dir, exist_ok=True)
    for filename in ["setup.sh","devcontainer.json"]:
        with open(os.path.join(devcontainer_dir,filename),"w") as f:
            f.write(static.read_resource(filename))
    # copy dashboard notebook, bank manifest, README
    for filename in ["bank.xml","README.md"]:
        with open(os.path.join(directory,filename),"w") as f:
            f.write(static.read_resource(filename))
    # copy gitignore
    with open(os.path.join(directory,".gitignore"),"w") as f:
        f.write(static.read_resource("gitignore.txt"))
    # generate requirements.txt
    with open(os.path.join(directory,"requirements.txt"),"w") as f:
        f.write(f"checkit-dashboard == {VERSION}")
    print(f"Successfully created new CheckIt bank in `{directory}`")


# checkit generate
@main.command(
    short_help="generate bank json",
)
@click.option(
    "-a",
    "--amount",
    default=1_000,
    help="Amount of exercises to generate.",
)
@click.option(
    "-r",
    "--regenerate",
    is_flag=True,
    help="Force regeneration of previously generated seeds.",
)
@click.option(
    "-i",
    "--images",
    is_flag=True,
    help="Generate images.",
)
@click.option(
    "-o",
    "--outcome",
    default="ALL",
    help="Outcome to generate. \"ALL\" generates all outcomes",
)
def generate(amount,regenerate,images,outcome):
    b = bank.Bank()
    if outcome != "ALL":
        b._outcomes = [o for o in b._outcomes if o.slug.lower() == outcome.lower()]
    b.generate_exercises(regenerate=regenerate,images=images,amount=amount)
    b.write_json()

# checkit viewer
@main.command(
    short_help="generate bank viewer",
)
@click.option(
    "-c",
    "--cache",
    is_flag=True,
    help="Include cache.",
)
def viewer(cache):
    bank.Bank().build_viewer(with_cache=cache)

# checkit cache
@main.command(
    short_help="download cache",
)
@click.argument('url')
def cache(url):
    for o in bank.Bank().outcomes():
        o.download_cache(url)


if __name__ == "__main__":
    main()
