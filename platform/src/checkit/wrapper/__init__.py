import importlib.resources
import subprocess

def sage(generator_path,output_path,preview=True):
    """
    Wraps generator and builds to a seeds.json file at output_path
    """
    if preview:
        preview_s = "preview"
    else:
        preview_s = "build"
    with importlib.resources.path("checkit.wrapper", "wrapper.sage") as wrapper_path:
        subprocess.run([
            "sage",
            wrapper_path,
            generator_path,
            output_path,
            preview_s,
        ])

    