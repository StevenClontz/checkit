# CheckIt Platform

A platform for authoring free and open randomized exercises for practice and assessment.
Includes the Python/Sagemath **CheckIt Dashboard** for authoring and generating random exercises,
and the TypeScript **CheckIt Viewer** for publishing exercise banks online.

Homepage at [checkit.clontz.org](https://checkit.clontz.org).
Documentation for authors and developers
is available in the [wiki on GitHub](https://github.com/StevenClontz/checkit/wiki).

## Package Development

### Python

Development uses `pyenv`:

<https://github.com/pyenv/pyenv>

with `pyenv-virtualenv`:

<https://github.com/pyenv/pyenv-virtualenv>.

Run the following, replacing `PYTHON_VERSION` with the version defined in
the `platform/src/checkit/static/PYTHON_VERSION` file.

```
pyenv install PYTHON_VERSION
pyenv virtualenv PYTHON_VERSION checkit
```

The virtual environment for this project can be activated
automatically in directories with a
`.python-version` file with the contents `checkit` by following
instructions at
<https://github.com/pyenv/pyenv-virtualenv#activate-virtualenv>.
Or use `pyenv activate checkit` and `pyenv deactivate` to do
this manually.

Now to install the in-development package into the virtual
environment.

```
pyenv virtualenvs # should show `* checkit` (note the `*`)
python -V # should show value of PYTHON_VERSION
python -m pip install --upgrade pip
python -m pip install -e dashboard[dev]
```

To enable this virtual environment for use as a Jupyter kernel for
the dashboard:

```
python -m ipykernel install --user --name=checkit --display-name "CheckIt Platform"
```

## Demo Bank

To be able to use the dashboard in the demo bank without affecting the Git repo,
run 

```
git update-index --skip-worktree demo-bank/dashboard.ipynb
```

Of course if you really need to update the dashboard:

```
git update-index --no-skip-worktree demo-bank/dashboard.ipynb
```

And to refresh the dashboard:

```
git update-index --no-skip-worktree demo-bank/dashboard.ipynb
git checkout demo-bank/dashboard.ipynb
git update-index --skip-worktree demo-bank/dashboard.ipynb
```
