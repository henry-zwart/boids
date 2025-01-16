# Python Boids

An interactive 3D simulation of [Craig Reynolds' 'Boids'](https://www.red3d.com/cwr/boids/) model, written in Python.

https://github.com/user-attachments/assets/74c8d25f-7a36-4b6e-9615-411b9d3c26d0

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

> [!IMPORTANT]
> If your Python3.13 executable is called something other than `python3.13`, replace this accordingly in the following steps.

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

## Boids

The Boids model simulates flocking behaviour observed in birds using three local
rules outlined first by Reynolds: 

+ **Avoidance:** Boids steer to avoid collisions with other nearby boids
+ **Cohesion:** Boids steer in the direction of the center-of-mass of nearby boids
+ **Alignment:** Boids attempt to match velocity with nearby boids

The application includes two further rules:

+ **Wall-avoidance:** Boids close to a boundary in some dimension accelerate away from the boundary at a constant acceleration 
+ **Flee:** Boids steer away from nearby predators

For a given boid, the acceleration due to each rule (aside from avoidance) is calculated with respect to the 
boids within the *view radius* of the given boid. The **avoidance** rule uses a separate *avoid radius*,
which is smaller than the view radius by default.

At each timestep, each boid's instantaneous acceleration is calculated as a weighted combination 
of the above rules. The resulting changes in velocity and position are calculated for a boid, $b$, as:

$$v_b(t + \Delta t) = v_b(t) + a_b(t)\cdot \Delta t$$

and 

$$x_b(t + \Delta t) = x_b(t) + v_b(t + \Delta t) \cdot \Delta t$$

Where the velocity at each step is bounded such that the speed lies in the 
(paramererisable) allowable range.



### Predators

The application includes a rudimentary predator implementation. Predators are driven 
by a single rule which steers them toward the center of mass of the boid population. The
strength of this rule is determined by the **seek** parameter (tunable within the application).
Higher values permit higher acceleration, which affects both the speed of predators, and 
the rate at which they can 'turn'. 

Aside from the boids' **flee** rule, which steers them away from predators within their
view radius, the predators have no further impact on the system (e.g. removal of collided 
boids). While the predator mechanics are fairly simple, we find the resulting dynamics
to be interesting. 

### Inspiration

The rule implementations draw inspiration from Craig Reynolds' [extended discussion on steering](https://www.red3d.com/cwr/steer/gdc99/),
Conrad Parker's [pseudocode](https://vergenet.net/~conrad/boids/pseudocode.html), and 
Cornell University's [ECE 4760 Boids project page](https://people.ece.cornell.edu/land/courses/ece4760/labs/s2021/Boids/Boids.html#:~:text=Boids%20is%20an%20artificial%20life,very%20simple%20set%20of%20rules.).

This implementation differs particularly from the above-mentioned discussions in that 
both the velocity and position are updated in accordance with the step-size. This results
in consistent simulation behaviour irrespective of the framerate (for sufficiently high
framerates, e.g. greater than $10fps$).

## License

[MIT](https://choosealicense.com/licenses/mit/)
