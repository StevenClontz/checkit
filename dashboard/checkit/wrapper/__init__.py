import importlib.resources
import subprocess, os, tempfile, shutil
from ..utils import working_directory

def sage(outcome,images=False,amount=1_000,random=False):
    """
    Wraps generator and builds to a seeds.json file at output_path
    """
    if not os.path.isfile(outcome.generator_path()):
        raise FileNotFoundError(outcome.generator_path())
    with importlib.resources.path("checkit.wrapper", "wrapper.sage") as wrapper_path:
        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copyfile(wrapper_path,os.path.join(tmpdir,"wrapper.sage"))
            with working_directory(outcome.bank.abspath()):
                cmds = [
                    "sage",
                    os.path.join(tmpdir,"wrapper.sage"),
                    outcome.generator_path(),
                    outcome.bank.build_path(),
                    outcome.slug,
                    "--amount",
                    str(amount),
                ]
                if random:
                    cmds += ["--random"]
                if images:
                    cmds += ["--gen_images"]
                subprocess.run(cmds,check=True)
