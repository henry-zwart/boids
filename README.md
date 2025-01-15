# Python Boids

An interactive 3D simulation of Craig Reynolds' 'Boids' model, written in Python.


https://github.com/user-attachments/assets/74c8d25f-7a36-4b6e-9615-411b9d3c26d0

## Running the application

The application is driven by a minimal command line interface with usage:

`boids [-h] [--framerate FRAMERATE] n_boids`

This opens a fullscreen window displaying the application.

Typical values for `n_boids` are between 500 and 1500. Above this limit the application 
reaches performance limits. Simulations above 1500 boids are possible, but must generally
trade off between lower framerate, or non-realtime simulation.

`--framerate` is an optional parameter which is otherwise defaulted based on `n_boids`.
If you experience slow or "jumpy" behaviour in the animation, particularly for large 
numbers of boids, you may try lowering the framerate.

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

## License

[MIT](https://choosealicense.com/licenses/mit/)
