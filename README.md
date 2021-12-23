# CheckIt Platform

A platform for authoring free and open randomized exercises for practice and assessment.
Includes the Python/Sagemath **CheckIt Platform** for authoring and generating random exercises,
and the TypeScript **CheckIt Viewer** for publishing exercise banks online, such as at
[CheckIt.clontz.org](https://checkit.clontz.org).

Documentation for authors and developers
is available in the [wiki on GitHub](https://github.com/StevenClontz/checkit/wiki).

## Package Development

### Python

Development uses `pyenv` with `pyenv-virtualenv`:
<https://github.com/pyenv/pyenv-virtualenv>.
Run the following, replacing `PYTHON_VERSION` with the version defined in
the `PYTHON_VERSION` file.

```
pyenv install PYTHON_VERSION
pyenv virtualenv PYTHON_VERSION checkit
```

Then the virtual environment for this project activates
either automatically or manually based on
<https://github.com/pyenv/pyenv-virtualenv#activate-virtualenv>.

```
pyenv local # should show `checkit`
python -m pip install -e platform[dev]
```

To enable this virtual environment for use as a Jupyter kernel for
the dashboard:

```
python -m ipykernel install --user --name=checkit --display-name "CheckIt Platform"
```

