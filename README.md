# CheckIt Platform

A platform for authoring free and open randomized exercises for practice and assessment.
Includes the Python/Sagemath **CheckIt Dashboard** for authoring and generating random exercises,
and the TypeScript **CheckIt Viewer** for publishing exercise banks online.

```
python -m pip install --upgrade pip
python -m pip install --upgrade checkit-dashboard
```

Homepage at [checkit.clontz.org](https://checkit.clontz.org).

Documentation for authors and developers
is available in the [wiki on GitHub](https://github.com/StevenClontz/checkit/wiki).

## Package Development

All dependencies are installed automatically when using a Codespace.
On GitHub, click "Code", select "Codespaces", then click "Create codespace on main".
For local installation, run `.devcontainer/setup.sh` and refer to
`.devcontainer/devcontainer.json` for other configurations.

### Build & deploy package

Make sure versions are set as intended! Then...

```
cd dashboard
python update_viewer.py
rm -rf dist/*
python -m build
python -m twine upload dist/*
```

### Updating docs

Just `python build_docs.py`.

