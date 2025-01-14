import sys

from .model import Flock
from .animation import InteractiveAnimation


# def draw_boids_3d(
#    frame: int,
#    flock: Flock,
#    scat: PathCollection,
#    pred: PathCollection,
#    ax: Axes3D,
#    velocities: Quiver | None,
#    accelerations: Quiver | None,
#    neighborhoods: list[Circle] | None,
#    avoid_radii: list[Circle] | None,
#    interval: float,
#    n_draw: int | None = None,
# ):
#    flock.update(interval)
#    n_draw = n_draw or len(flock.position)
#    scat._offsets3d = flock.position[:n_draw].T
#    pred._offsets3d = flock.predator_position.T
#    if velocities is not None:
#        velocities.set_offsets(flock.position[:n_draw])
#        velocities.set_UVC(flock.velocity[:n_draw, 0], flock.velocity[:n_draw, 1])
#    if accelerations is not None:
#        accelerations.set_offsets(flock.position[:n_draw])
#        accelerations.set_UVC(
#            flock.acceleration[:n_draw, 0] * interval,
#            flock.acceleration[:n_draw, 1] * interval,
#        )
#    if neighborhoods is not None:
#        for i, n in enumerate(neighborhoods[:n_draw]):
#            n.set_center(flock.position[i])
#    if avoid_radii is not None:
#        for i, n in enumerate(avoid_radii[:n_draw]):
#            n.set_center(flock.position[i])
#    ax.view_init(elev=15, azim=frame / 6)
#
#
# def draw_boids(
#    frame: int,
#    flock: Flock,
#    scat: PathCollection,
#    pred: PathCollection,
#    velocities: Quiver | None,
#    accelerations: Quiver | None,
#    neighborhoods: list[Circle] | None,
#    avoid_radii: list[Circle] | None,
#    interval: float,
#    n_draw: int | None = None,
# ):
#    flock.update(interval)
#    n_draw = n_draw or len(flock.position)
#    scat.set_offsets(flock.position[:n_draw])
#    pred.set_offsets(flock.predator_position)
#    if velocities is not None:
#        velocities.set_offsets(flock.position[:n_draw])
#        velocities.set_UVC(flock.velocity[:n_draw, 0], flock.velocity[:n_draw, 1])
#    if accelerations is not None:
#        accelerations.set_offsets(flock.position[:n_draw])
#        accelerations.set_UVC(
#            flock.acceleration[:n_draw, 0] * interval,
#            flock.acceleration[:n_draw, 1] * interval,
#        )
#    if neighborhoods is not None:
#        for i, n in enumerate(neighborhoods[:n_draw]):
#            n.set_center(flock.position[i])
#    if avoid_radii is not None:
#        for i, n in enumerate(avoid_radii[:n_draw]):
#            n.set_center(flock.position[i])
#
#
# def animate_flock_3d(
#    flock: Flock,
#    fps: int,
#    seconds: int,
#    bounds: list[int],
#    rate: float = 1.0,
#    show_velocity: bool = True,
#    show_acceleration: bool = True,
#    show_neighborhoods: bool = False,
# ):
#    fig = plt.figure()
#
#    # ax = fig.add_subplot(111, projection="3d")
#    ax = fig.add_subplot(1, 6, (1, 3), projection="3d")
#    ax.set_aspect("equal")
#    ax.set_xlim(0, bounds[0])
#    ax.set_ylim(0, bounds[1])
#    scat = ax.scatter(*flock.position.T, s=1, color="blue")
#    pred = ax.scatter(*flock.predator_position.T, s=15, color="red")
#
#    # ax_speed = plt.axes([0.1, 0.05, 0.35, 0.03])
#    ax_minspeed = plt.axes([0.7, 0.75, 0.2, 0.03])
#    s_minspeed = Slider(
#        ax_minspeed, "Min speed", 0, 400, valinit=flock.min_speed, valstep=5
#    )
#    ax_maxspeed = plt.axes([0.7, 0.7, 0.2, 0.03])
#    s_maxspeed = Slider(
#        ax_maxspeed,
#        "Max speed",
#        0,
#        400,
#        valinit=flock.max_speed,
#        valstep=5,
#        slidermin=s_minspeed,
#    )
#
#    ax_kill_predator = plt.axes([0.7, 0.5, 0.1, 0.05])
#    btn_kill_predator = Button(ax_kill_predator, "- Pred")
#
#    ax_add_predator = plt.axes([0.82, 0.5, 0.1, 0.05])
#    btn_add_predator = Button(ax_add_predator, "+ Pred")
#
#    def update_minspeed(val):
#        flock.min_speed = s_minspeed.val
#
#    def update_maxspeed(val):
#        flock.max_speed = s_maxspeed.val
#
#    def add_predator(val):
#        flock.add_predator()
#
#    def kill_predator(val):
#        flock.remove_oldest_predator()
#
#    s_minspeed.on_changed(update_minspeed)
#    s_maxspeed.on_changed(update_maxspeed)
#    btn_add_predator.on_clicked(add_predator)
#    btn_kill_predator.on_clicked(kill_predator)
#
#    if show_velocity:
#        velocity_arrows = ax.quiver(
#            flock.position[:, 0],
#            flock.position[:, 1],
#            flock.velocity[:, 0],
#            flock.velocity[:, 1],
#            # angles="xy",
#            scale_units="xy",
#            scale=1,
#            color="green",
#            width=0.003,
#        )
#    else:
#        velocity_arrows = None
#
#    if show_acceleration:
#        acceleration_arrows = ax.quiver(
#            flock.position[:, 0],
#            flock.position[:, 1],
#            flock.acceleration[:, 0],
#            flock.acceleration[:, 1],
#            # angles="xy",
#            scale_units="xy",
#            scale=1,
#            color="blue",
#            width=0.003,
#        )
#    else:
#        acceleration_arrows = None
#
#    if show_neighborhoods:
#        neighborhoods = [
#            Circle(
#                (x, y),
#                radius=flock.view_radius,
#                fill=False,
#                edgecolor="grey",
#                linestyle="--",
#            )
#            for (x, y) in flock.position
#        ]
#        avoid_radii = [
#            Circle(
#                (x, y),
#                radius=flock.avoid_radius,
#                fill=False,
#                edgecolor="red",
#                linestyle="--",
#            )
#            for (x, y) in flock.position
#        ]
#        for n in itertools.chain(neighborhoods, avoid_radii):
#            ax.add_patch(n)
#    else:
#        neighborhoods = []
#        avoid_radii = []
#
#    draw_fn = partial(
#        draw_boids_3d,
#        flock=flock,
#        scat=scat,
#        pred=pred,
#        ax=ax,
#        velocities=velocity_arrows,
#        accelerations=acceleration_arrows,
#        neighborhoods=neighborhoods,
#        avoid_radii=avoid_radii,
#        interval=1 / fps,
#    )
#    ani = FuncAnimation(
#        fig=fig,
#        func=draw_fn,
#        frames=fps * seconds,
#        interval=(1000 / rate) / fps,
#        repeat=False,
#    )
#    return fig, ax, ani, (s_minspeed, s_maxspeed, btn_add_predator, btn_kill_predator)
#
#
# def animate_flock(
#    flock: Flock,
#    fps: int,
#    seconds: int,
#    bounds: list[int],
#    rate: float = 1.0,
#    show_velocity: bool = True,
#    show_acceleration: bool = True,
#    show_neighborhoods: bool = False,
# ):
#    fig, ax = plt.subplots()
#    ax.set_aspect("equal")
#    ax.set_xlim(0, bounds[0])
#    ax.set_ylim(0, bounds[1])
#    scat = ax.scatter(*flock.position.T, s=5, color="blue")
#    pred = ax.scatter(*flock.predator_position.T, s=15, color="red")
#
#    if show_velocity:
#        velocity_arrows = ax.quiver(
#            flock.position[:, 0],
#            flock.position[:, 1],
#            flock.velocity[:, 0],
#            flock.velocity[:, 1],
#            # angles="xy",
#            scale_units="xy",
#            scale=1,
#            color="green",
#            width=0.003,
#        )
#    else:
#        velocity_arrows = None
#
#    if show_acceleration:
#        acceleration_arrows = ax.quiver(
#            flock.position[:, 0],
#            flock.position[:, 1],
#            flock.acceleration[:, 0],
#            flock.acceleration[:, 1],
#            # angles="xy",
#            scale_units="xy",
#            scale=1,
#            color="blue",
#            width=0.003,
#        )
#    else:
#        acceleration_arrows = None
#
#    if show_neighborhoods:
#        neighborhoods = [
#            Circle(
#                (x, y),
#                radius=flock.view_radius,
#                fill=False,
#                edgecolor="grey",
#                linestyle="--",
#            )
#            for (x, y) in flock.position
#        ]
#        avoid_radii = [
#            Circle(
#                (x, y),
#                radius=flock.avoid_radius,
#                fill=False,
#                edgecolor="red",
#                linestyle="--",
#            )
#            for (x, y) in flock.position
#        ]
#        for n in itertools.chain(neighborhoods, avoid_radii):
#            ax.add_patch(n)
#    else:
#        neighborhoods = []
#        avoid_radii = []
#
#    draw_fn = partial(
#        draw_boids,
#        flock=flock,
#        scat=scat,
#        pred=pred,
#        velocities=velocity_arrows,
#        accelerations=acceleration_arrows,
#        neighborhoods=neighborhoods,
#        avoid_radii=avoid_radii,
#        interval=1 / fps,
#    )
#    ani = FuncAnimation(
#        fig=fig,
#        func=draw_fn,
#        frames=fps * seconds,
#        interval=(1000 / rate) / fps,
#        repeat=False,
#    )
#    return fig, ax, ani
#
#
# def test_wall_avoidance():
#    DIMS = [20, 50]
#    flock = Flock(
#        n_boids=1,
#        bounds=DIMS,
#        max_speed=4,
#        min_speed=3,
#    )
#    flock.position = np.array([[5, 2.5]], dtype=np.float64)
#    flock.velocity = np.array([[2, 0.1]], dtype=np.float64)
#    _ = animate_flock(flock, fps=30, seconds=30, bounds=DIMS, show_neighborhoods=True)
#    plt.show()
#
#
# def test_avoidance():
#    DIMS = [20, 10]
#    flock = Flock(
#        n_boids=2,
#        bounds=DIMS,
#        weights=Weights(separation=30.0, cohesion=0.0, alignment=0.0),
#        view_radius=3,
#        avoid_radius=1.5,
#        initial_position=np.array([[10, 0], [DIMS[0], 0]], dtype=np.float64),
#        initial_velocity=np.array([[1, 1], [-1, 1]], dtype=np.float64),
#    )
#    fig, ax, ani = animate_flock(
#        flock, fps=30, rate=0.1, seconds=30, bounds=DIMS, show_neighborhoods=True
#    )
#    plt.show()
#
#
# def test_alignment():
#    DIMS = [10, 20]
#    flock = Flock(
#        n_boids=5,
#        bounds=DIMS,
#        weights=Weights(separation=0.0, cohesion=0.0, alignment=3),
#        view_radius=2.5,
#        avoid_radius=1.0,
#        initial_position=np.array(
#            [[1.0, 10.0], [8, 2.5], [7.5, 2.0], [8.5, 2.0], [7, 1.5]], dtype=np.float64
#        ),
#        initial_velocity=np.array(
#            [[1.0, 0.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]],
#            dtype=np.float64,
#        ),
#    )
#    fig, ax, ani = animate_flock(
#        flock, fps=30, rate=0.1, seconds=30, bounds=DIMS, show_neighborhoods=True
#    )
#    plt.show()
#
#
# def test_cohesion():
#    DIMS = [10, 20]
#    flock = Flock(
#        n_boids=5,
#        bounds=DIMS,
#        weights=Weights(separation=0.0, cohesion=0.3, alignment=0.0),
#        view_radius=5,
#        initial_position=np.array(
#            [[1.0, 10.0], [8, 1.5], [7.5, 1.0], [8.5, 1.0], [7, 0.5]], dtype=np.float64
#        ),
#        initial_velocity=np.array(
#            [[1.0, 0.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]],
#            dtype=np.float64,
#        ),
#    )
#    fig, ax, ani = animate_flock(flock, fps=30, rate=0.1, seconds=30, bounds=DIMS)
#    plt.show()
#
#
# def test_joust():
#    DIMS = [20, 10]
#    flock = Flock(
#        n_boids=2,
#        bounds=DIMS,
#        weights=Weights(separation=0.0, cohesion=1.0, alignment=0.0),
#        view_radius=3,
#        initial_position=np.array([[2, 4], [18, 6]], dtype=np.float64),
#        initial_velocity=np.array([[0.1, 0], [-0.1, 0]], dtype=np.float64),
#    )
#    fig, ax, ani = animate_flock(
#        flock, fps=30, rate=1, seconds=30, bounds=DIMS, show_neighborhoods=True
#    )
#    plt.show()


def run():
    DIMS = [1024, 1024, 1024]
    n_boids = int(sys.argv[1])

    if n_boids <= 512:
        fps = 30
        view_radius = 150
    elif n_boids <= 1500:
        fps = 15
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
