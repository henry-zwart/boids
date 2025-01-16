import argparse


from .model import Flock
from .animation import InteractiveAnimation

DIMS = [1024, 1024, 1024]


def set_default_fps(n_boids: int) -> int:
    """Configure default framerate heuristically to ensure stable animation."""
    if n_boids <= 512:
        return 30
    elif n_boids <= 1024:
        return 25
    elif n_boids <= 1500:
        return 20
    else:
        return 15


def set_default_view_radius(n_boids: int) -> int:
    """Configure default view radius to ensure stable animation."""
    if n_boids <= 1500:
        return 150
    else:
        return 50


def run():
    """A minimal CLI to drive the boids application."""
    parser = argparse.ArgumentParser("Interactive Boid simulation.")
    parser.add_argument("n_boids", type=int, help="Number of boids to simulate.")
    parser.add_argument(
        "--framerate",
        type=int,
        default=None,
        help="Frames per second (FPS). If not specified, simulation uses a default based on n_boids.",
    )

    args = parser.parse_args()
    n_boids = args.n_boids
    fps = args.framerate or set_default_fps(n_boids)
    view_radius = set_default_view_radius(n_boids)

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
