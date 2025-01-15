# Python Boids

An interactive 3D simulation of Craig Reynolds' 'Boids' model, written in Python.

https://github.com/user-attachments/assets/74c8d25f-7a36-4b6e-9615-411b9d3c26d0

## Boids

The Boids model simulates flocking behaviour observed in birds using three local
rules outlined first by Reynolds: 

+ Avoidance: Boids steer to avoid collisions with other nearby boids
+ Cohesion: Boids steer in the direction of the center-of-mass of nearby boids
+ Alignment: Boids attempt to match velocity with nearby boids

The application includes two further rules:

+ Wall-avoidance: Boids close to a boundary in some dimension accelerate away from the boundary at a constant acceleration
+ Flee: Boids steer away from nearby predators

For a given boid, the acceleration due to each rule (aside from avoidance) is calculated with respect to the 
boids within the *view radius* of the given boid. The **avoidance** rule uses a separate *avoid radius*,
which is smaller than the view radius by default.

At each timestep, each boid's instantaneous acceleration is calculated as a weighted combination 
of the above rules. The resulting changes in velocity and position are calculated as 
$v(t + \delta t, b) = v(t, b) + a(t, b)\cdot \delta t$ and $x(t + \delta t, b) = x(t, b) + v(t + \delta t, b)\cdot \delta t$.

### Predators

The application includes a rudimentary predator implementation. Predators are driven 
by a single rule which steers them toward the center of mass of the boid population. 

Aside from the boids' **flee** rule, which steers them away from predators within their
view radius, the predators have no further impact on the system (e.g. removal of collided 
boids). While the predator mechanics are fairly simple, we find the resulting dynamics
to be interesting. 


## Usage

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
Alternatively, you can also run the application within a virtual environment. This method 
requires a pre-existing installation of Python3.13, for instance, obtained via conda or pyenv. 

### Running with uv (recommended)

```zsh
# == Navigate to this directory
cd /path/to/boids

# == Run the model, passing the number of boids as a parameter
uv run boids 512
```

### Running with a generic Python3.13 venv

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
