import numpy as np
from dataclasses import dataclass

from scipy.spatial import KDTree


@dataclass
class Weights:
    separation: float = 20 * 3.5
    alignment: float = 20 / 15
    cohesion: float = 1 / 10
    flee: float = 20.0
    containment: float = 1.0
    predator_seek: float = 1.0


class Flock:
    def __init__(
        self,
        n_boids: int,
        n_predators: int = 0,
        min_speed: float = 4,
        max_speed: float = 5,
        predator_min_speed: float = 4,
        predator_max_speed: float = 10,
        view_radius: float = 10,
        avoid_radius: float = 3,
        weights: Weights | None = None,
        bounds: list[int] | None = None,
        barrier_pct: float = 5,
        initial_position: np.ndarray | None = None,
        initial_velocity: np.ndarray | None = None,
        rng: np.random.RandomState | None = None,
        random_seed: int | None = None,
    ):
        self.rng = rng or np.random.default_rng(random_seed)
        self.weights = weights or Weights()
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.predator_min_speed = predator_min_speed
        self.predator_max_speed = predator_max_speed
        self.view_radius = view_radius
        self.avoid_radius = avoid_radius

        self.init_environment(bounds, barrier_pct)
        self.init_agents(n_boids, n_predators, initial_position, initial_velocity)

    def init_environment(self, bounds: list[int] | None, barrier_pct: float):
        """Compute the bounds and margins for boid containment."""
        if bounds is not None:
            self.ndim = len(bounds)
            self.bounds = np.array([0 for _ in range(self.ndim)] + bounds)
        else:
            self.ndim = 2
            self.bounds = np.array([0, 0, 50, 50])
        self.barrier_pct = barrier_pct / 100
        self.barrier_bounds = self.bounds.copy().astype(np.float64)
        self.barrier_bounds[: self.ndim] += self.bounds[self.ndim :] * self.barrier_pct
        self.barrier_bounds[self.ndim :] *= 1 - self.barrier_pct

    def init_agents(
        self,
        n_boids: int,
        n_predators: int,
        boid_initial_position: np.ndarray | None,
        boid_initial_velocity: np.ndarray | None,
    ):
        """Initialise boid and predator position, velocity, and acceleration."""
        # boid position + velocity
        self.position = self.init_positions(n_boids, boid_initial_position)
        self.velocity = self.init_velocity(
            n_boids, boid_initial_velocity, self.min_speed, self.max_speed
        )

        # predator position + velocity
        self.predator_position = self.init_positions(n_predators, None)
        self.predator_velocity = self.init_velocity(
            n_predators, None, self.predator_min_speed, self.predator_max_speed
        )

        # Initialise acceleration arrays, and compute initial values
        self.acceleration = np.zeros_like(self.velocity)
        self.predator_acceleration = np.zeros(
            (n_predators, self.ndim), dtype=np.float64
        )
        self.compute_acceleration()

    def init_positions(
        self, n_agents: int, initial_position: np.ndarray | None
    ) -> np.ndarray:
        """Generate boid positions within the barrier."""
        if initial_position is not None:
            position = initial_position
        else:
            normalised_positions = self.rng.random(size=(n_agents, self.ndim))
            non_barrier_dims = (1 - 2 * self.barrier_pct) * self.bounds[self.ndim :]
            min_barrier = self.barrier_pct * self.bounds[self.ndim :]
            position = normalised_positions * non_barrier_dims + min_barrier
        return position

    def init_velocity(
        self,
        n_agents: int,
        initial_velocity: np.ndarray | None,
        min_speed: float,
        max_speed: float,
    ) -> np.ndarray:
        """Initialise velocity for boids or predators.

        Initial velocity is calculated as the combination of an initial speed and
        initial heading. The initial speed is bounded to be within the allowable range.
        """
        if initial_velocity is not None:
            velocity = bound_norm(initial_velocity, min_speed, max_speed)
        else:
            speed = self.rng.random(size=n_agents) * (max_speed - min_speed) + min_speed
            heading = (self.rng.random(size=(n_agents, self.ndim)) * 2) - 1
            heading /= np.linalg.norm(heading, axis=1)[..., None]
            velocity = heading * speed[..., None]
        return velocity

    def update(self, step_size: float = 1):
        """Update the velocity and position of all agents, over a given timestep.

        New velocity is calculated as: old_velocity + acceleration * step_size
        New position is calculated as: old_position + new_velocity * step_size

        Where the velocity is scaled such that the speed falls within the allowable range.
        """
        # Update boids
        self.velocity = bound_norm(
            self.velocity + self.acceleration * step_size,
            self.min_speed,
            self.max_speed,
        )
        self.position += self.velocity * step_size

        # Update predators
        self.predator_velocity = bound_norm(
            self.predator_velocity + self.predator_acceleration * step_size,
            self.predator_min_speed,
            self.predator_max_speed,
        )
        self.predator_position += self.predator_velocity * step_size

        self.compute_acceleration()

    def compute_acceleration(self):
        """Compute instantaneous acceleration for all agents (boids and predators).

        Boid acceleration is a weighted combination of:
        - Avoidance: away from boids within self.avoid_radius
        - Cohesion: toward the center of mass of boids in self.view_radius
        - Alignment: match velocity (speed and heading) of boids in self.view_radius
        - Wall-avoidance: away from walls when margin is within self.avoid_radius
        - Flee: away from predators within self.view_radius

        Predator acceleration is given by the cohesion rule, calculated across all
        boids (effective infinite view_radius).

        A KDTree is used to avoid the poor scaling associated with the naive calculation
        of nearby birds. This KDTree is rebuilt each time the function is called.

        While its use provides a significant performance increase for large numbers of boids,
        the KDTree building and lookup still consumes most of the method runtime. A
        future direction for performance improvement is described in the README.
        """
        self.acceleration[:, :] = 0
        self.predator_acceleration[:, :] = 0

        kdtree = KDTree(self.position)

        too_close = kdtree.query_ball_tree(
            kdtree,
            r=self.avoid_radius,
        )
        within_sight = kdtree.query_ball_tree(
            kdtree,
            r=self.view_radius,
        )
        for b in range(len(self)):
            # Separation
            avoidance = self.calculate_avoidance(
                self.position[b], self.position[too_close[b]]
            )
            alignment = self.calculate_alignment(
                self.velocity[b], self.velocity[within_sight[b]]
            )
            cohesion = self.calculate_cohesion(
                self.position[b], self.position[within_sight[b]]
            )

            self.acceleration[b] = (
                avoidance * self.weights.separation
                + alignment * self.weights.alignment
                + cohesion * self.weights.cohesion
            )

        self.acceleration += self.avoid_walls()

        # Add flee affect per predator
        for p in range(len(self.predator_position)):
            # Steer toward the center of mass of boids
            center_of_mass = self.position.mean(axis=0)
            seek = center_of_mass - self.predator_position[p]
            self.predator_acceleration[p] = seek * self.weights.predator_seek

            # Steer each nearby boid away from predator
            nearby_boids = kdtree.query_ball_point(
                self.predator_position[p], self.view_radius
            )
            if len(nearby_boids) > 0:
                flee = (self.position[nearby_boids] - self.predator_position[p]).sum(
                    axis=0
                )
                flee /= np.linalg.norm(flee)
                self.acceleration[nearby_boids] += (
                    flee * self.weights.flee * self.max_speed
                )

    def calculate_avoidance(
        self, position: np.ndarray, position_close: np.ndarray
    ) -> np.ndarray:
        """Calculate avoidance force.

        This is calculated by summing vectors directed away from nearby boids.
        """
        return (position - position_close).sum(axis=0)

    def calculate_alignment(
        self, velocity: np.ndarray, velocity_close: np.ndarray
    ) -> np.ndarray:
        """Calculate alignment force.

        Determines the average velocity of nearby boids, and takes the alignment
        force to be the vector in the direction of this average velocity, from the
        current velocity.

        Note that the velocity_close parameter includes the velocity of the
        target boid. The calculation thus subtracts this velocity inside the average
        velocity calculation.
        """
        return (
            (velocity_close.sum(axis=0) - velocity)
            / max(1, (velocity_close.shape[0] - 1))
        ) - velocity

    def calculate_cohesion(
        self, position: np.ndarray, position_close: np.ndarray
    ) -> np.ndarray:
        """Calculate cohesion force.

        Determines the center-of-mass of nearby boids, and takes the cohesion
        force to be the vector in the direction of this center-of-mass, from the
        current position.

        Note that the position_close parameter includes the position of the
        target boid. The calculation thus subtracts this position inside the average
        center-of-mass calculation.
        """
        return (
            (position_close.sum(axis=0) - position)
            / max(1, (position_close.shape[0] - 1))
        ) - position

    def avoid_walls(self):
        """Calculate the wall-avoidance force across all boids in the simulation.

        A boid is accelerated away from a wall if the margin on that wall lies within
        the boid avoidance radius. The default margin extends 5% internal to the wall
        bounds. The acceleration away from any given wall is given by the product
        of the maximum boid speed and the wall avoidance weight.
        """
        nudge = np.zeros_like(self.acceleration)
        for dim in range(self.ndim):
            exit_left = (
                self.position[:, dim] - self.avoid_radius < self.barrier_bounds[dim]
            )
            exit_right = (
                self.position[:, dim] + self.avoid_radius
                > self.barrier_bounds[self.ndim + dim]
            )
            nudge[exit_left, dim] = 1
            nudge[exit_right, dim] = -1

        return nudge * self.max_speed * self.weights.containment

    def add_predator(self):
        """Adds a predator to the system with random initial position and velocity."""
        position = self.init_positions(1, None)
        velocity = self.init_velocity(
            1, None, self.predator_min_speed, self.predator_max_speed
        )
        acceleration = np.zeros((1, self.ndim), dtype=np.float64)
        self.predator_position = np.vstack([self.predator_position, position])
        self.predator_velocity = np.vstack([self.predator_velocity, velocity])
        self.predator_acceleration = np.vstack(
            [self.predator_acceleration, acceleration]
        )

    def remove_oldest_predator(self):
        """Removes the predator in index 0 from the system.

        If no predators exist, this method has no effect.
        """
        self.predator_position = self.predator_position[1:]
        self.predator_velocity = self.predator_velocity[1:]
        self.predator_acceleration = self.predator_acceleration[1:]

    def __len__(self) -> int:
        return len(self.position)


def bound_norm(vec: np.ndarray, min_norm: float, max_norm: float) -> np.ndarray:
    """Scales a vector such that its norm is within an allowable range."""
    norm = np.linalg.norm(vec, axis=1)
    too_high = norm > max_norm
    too_low = norm < min_norm
    vec[too_high] = (vec[too_high] / norm[too_high, None]) * max_norm
    vec[too_low] = (vec[too_low] / norm[too_low, None]) * min_norm
    return vec
