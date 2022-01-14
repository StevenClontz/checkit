import importlib.resources
import subprocess
from ..utils import working_directory

def sage(outcome,output_path,preview=True):
    """
    Wraps generator and builds to a seeds.json file at output_path
    """
    if preview:
        preview_s = "preview"
    else:
        preview_s = "build"
    with importlib.resources.path("checkit.wrapper", "wrapper.sage") as wrapper_path:
        with working_directory(outcome.bank.abspath()):
            subprocess.run([
                "sage",
                wrapper_path,
                outcome.generator_path(),
                output_path,
                preview_s,
            ], check=True)

    