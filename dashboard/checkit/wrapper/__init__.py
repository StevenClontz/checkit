import importlib.resources
import subprocess, os
from ..utils import working_directory

def sage(outcome,output_path,preview=True,images=False):
    """
    Wraps generator and builds to a seeds.json file at output_path
    """
    if preview:
        preview_s = "preview"
    else:
        preview_s = "build"
    if not os.path.isfile(outcome.generator_path()):
        raise FileNotFoundError(outcome.generator_path())
    with importlib.resources.path("checkit.wrapper", "wrapper.sage") as wrapper_path:
        with working_directory(outcome.bank.abspath()):
            cmds = [
                "sage",
                wrapper_path,
                outcome.generator_path(),
                output_path,
                preview_s,
            ]
            if images:
                cmds += ["images"]
            subprocess.run(cmds,check=True)
