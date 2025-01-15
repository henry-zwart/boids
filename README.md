# Python Boids

An interactive 3D simulation of Craig Reynolds' 'Boids' model, written in Python.


https://github.com/user-attachments/assets/74c8d25f-7a36-4b6e-9615-411b9d3c26d0

## Running the application

The application is driven by a minimal command line interface with the following usage:

> `boids [-h] [--framerate FRAMERATE] n_boids`

Where `--framerate` is an optional parameter which is otherwise defaulted based on `n_boids`.
If you experience slow or "jumpy" behaviour in the animation, particularly for large 
numbers of boids, you may try lowering the framerate.

Typical values for `n_boids` are between 500 and 1500. Above this limit the application 
reaches performance limits. Simulations above 1500 boids are possible, but must generally
trade off between lower framerate, or non-realtime simulation.

The simplest way to run the application is via [uv](https://github.com/astral-sh/uv):

```zsh
# == Navigate to this directory
cd /path/to/boids

# == Run the model, passing the number of boids as a parameter
uv run boids 512
```

Alternatively, you can also run the application within a virtual environment. This method 
requires a pre-existing installation of Python3.13, for instance, obtained via conda or pyenv. 

> **Note:** If your Python3.13 executable is called something other than `python3.13`, replace this accordingly in the following steps.

```zsh
# == Navigate to this directory
cd path/to/boids

# == Create a virtual environment
python3.13 -m venv env

# == Activate the virtual environment (platform-specific)
source env/bin/activate # On macOS or Linux
.\env\Scripts\activate # On windows

# == Install package and dependencies
pip install .

# == Run the model, passing the number of boids as a parameter
python -m boids 512
```

This should open a fullscreen window with the interactive boids application.

## Development - Getting started
See the [assignment specification](assignment_spec.pdf).

This repository uses _uv_ to manage Python and its dependencies, and _pre-commit_ to run
automatic code linting & formatting.

1. Install [uv](https://github.com/astral-sh/uv)

2. Navigate to this project directory

3. Install pre-commit:

```zsh
# We can use uv to install pre-commit!
uv tool install pre-commit --with pre-commit-uv --force-reinstall

# Check that pre-commit installed alright (should say 3.8.0 or similar)
pre-commit --version

# After installing pre-commit, you'll need to initialise it.
# This installs all pre-commit hooks, the scripts which run before a commit.
pre-commit install

# It's a good idea to run pre-commit now on all files.
pre-commit run --all-files
```

4. Run code:

```zsh
uv run <PATH-TO-PYTHON-FILE>
```

## Pre-commit hooks

I've included a couple of pre-commit hooks 
(see [.pre-commit-config.yaml](.pre-commit-config.yaml)) which will be executed every 
time we commit code to git. Both pre-commit hooks come from the 
[ruff](https://github.com/astral-sh/ruff) Python linter:
- `ruff`: lints Python code to ensure it adheres to the PEP8 standards. Includes a bunch of nice things like automatic sorting of imports by name and type.
- `ruff format`: formats Python code in a consistent manner, including removing excess whitespace, swapping tabs for spaces, and a _tonne_ of other things.

These should help to keep code tidy and consistent, with no extra effort on our part. 
Both of the hooks should run automagically if you've followed the setup instructions for
[installing pre-commit with uv](#development---getting-started).

## License

[MIT](https://choosealicense.com/licenses/mit/)
