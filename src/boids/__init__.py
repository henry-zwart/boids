import sys

from .model import Flock
from .animation import InteractiveAnimation


def run():
    DIMS = [1024, 1024, 1024]
    n_boids = int(sys.argv[1])

    if n_boids <= 512:
        fps = 30
        view_radius = 150
    elif n_boids <= 1024:
        fps = 25
        view_radius = 150
    elif n_boids <= 1500:
        fps = 20
        view_radius = 150
    else:
        fps = 15
        view_radius = 50

    flock = Flock(
        n_boids=n_boids,
        bounds=DIMS,
        min_speed=130,
        max_speed=170,
        predator_min_speed=260,
        predator_max_speed=350,
        view_radius=view_radius,
        avoid_radius=20,
    )

    animation = InteractiveAnimation(flock, fps=fps)
    animation.run()


def main():
    run()
