from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt
from boids.model import Flock


class InteractiveAnimation:
    ROTATION_SPEED = 1 / 10

    def __init__(self, flock: Flock, fps: float = 30, show_axes: bool = True):
        self.flock = flock
        self.fps = fps
        self.step_size = 1 / fps
        self.show_axes = show_axes
        self.ndim = flock.ndim
        self.camera_orbit_enabled = True if self.ndim == 3 else False
        self.camera_orbit_frame = 0
        self.setup_plot()
        self.setup_widgets()

    def run(self):
        cycle_seconds = (360 / self.ROTATION_SPEED) / self.fps
        self.total_frames = int(self.fps * cycle_seconds)
        self.animation = FuncAnimation(
            fig=self.fig,
            func=self.update_plot,
            frames=self.total_frames,
            interval=1000 / self.fps,
            repeat=True,
            blit=True,
        )
        plt.show()

    def update_plot(self, frame: int):
        self.flock.update(self.step_size)
        self.boids.set_data(self.flock.position[:, 0], self.flock.position[:, 1])
        self.preds.set_data(
            self.flock.predator_position[:, 0], self.flock.predator_position[:, 1]
        )
        if self.ndim == 3:
            self.boids.set_3d_properties(self.flock.position[:, 2])
            self.preds.set_3d_properties(self.flock.predator_position[:, 2])

        if self.camera_orbit_enabled:
            self.ax_plot.view_init(
                elev=15, azim=self.camera_orbit_frame * self.ROTATION_SPEED
            )
            self.camera_orbit_frame += 1

        return self.boids, self.preds, self.ax_plot

    def setup_plot(
        self,
    ):
        fig = plt.figure(layout="constrained")

        # Create the axis for the plot
        if self.ndim == 2:
            ax_plot = fig.add_subplot(1, 12, (2, 5))
        elif self.ndim == 3:
            ax_plot = fig.add_subplot(1, 6, (1, 3), projection="3d", focal_length=0.3)
        else:
            raise ValueError("Only dimensions 2 and 3 are supported.")

        # Set axis scales and limits
        ax_plot.set_aspect("equal")
        ax_plot.set_xlim(0, self.flock.bounds[self.ndim + 0])
        ax_plot.set_ylim(0, self.flock.bounds[self.ndim + 1])
        ax_plot.tick_params(
            left=False, bottom=False, labelleft=False, labelbottom=False
        )

        if self.ndim == 3:
            ax_plot.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax_plot.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax_plot.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            ax_plot.set_zlim(0, self.flock.bounds[self.ndim + 2])

        if not self.show_axes:
            ax_plot.set_axis_off()

        # Plot the boids and the predators
        boid_size = 1 if self.flock.position.shape[0] > 1024 else 1.5
        (self.boids,) = ax_plot.plot(
            *self.flock.position.T,
            markersize=boid_size,
            marker="o",
            linestyle="",
        )
        (self.preds,) = ax_plot.plot(
            *self.flock.predator_position.T,
            markersize=5,
            color="red",
            marker="o",
            linestyle="",
        )

        # Add help text
        fig.text(0.02, 0.02, "(q) to quit", weight="bold")

        # Make the window fullscreen
        figManager = plt.get_current_fig_manager()
        figManager.full_screen_toggle()

        # Store plot in object
        self.fig = fig
        self.ax_plot = ax_plot

    def setup_widgets(self):
        # Rule weights
        self.fig.text(0.75, 0.8, "Rule weights", ha="center", va="center", fontsize=12)
        self.ax_separation_slider = self.fig.add_axes((0.65, 0.75, 0.2, 0.03))
        self.ax_alignment_slider = self.fig.add_axes((0.65, 0.72, 0.2, 0.03))
        self.ax_cohesion_slider = self.fig.add_axes((0.65, 0.69, 0.2, 0.03))
        self.ax_flee_slider = self.fig.add_axes((0.65, 0.66, 0.2, 0.03))
        self.ax_pred_seek_slider = self.fig.add_axes((0.65, 0.63, 0.2, 0.03))
        self.separation_slider = Slider(
            self.ax_separation_slider,
            "Separation",
            0,
            150,
            dragging=False,
            valinit=self.flock.weights.separation,
        )
        self.alignment_slider = Slider(
            self.ax_alignment_slider,
            "Alignment",
            0,
            10,
            dragging=False,
            valinit=self.flock.weights.alignment,
        )
        self.cohesion_slider = Slider(
            self.ax_cohesion_slider,
            "Cohesion",
            0,
            1,
            dragging=False,
            valinit=self.flock.weights.cohesion,
        )
        self.flee_slider = Slider(
            self.ax_flee_slider, "Flee", 0, 100, valinit=self.flock.weights.flee
        )
        self.seek_slider = Slider(
            self.ax_pred_seek_slider,
            "Seek (pred.)",
            0,
            5,
            dragging=False,
            valinit=self.flock.weights.predator_seek,
        )

        # Boid speed
        self.fig.text(0.75, 0.56, "Boid speed", ha="center", va="center", fontsize=12)
        self.ax_minspeed_slider = self.fig.add_axes((0.65, 0.51, 0.2, 0.03))
        self.ax_maxspeed_slider = self.fig.add_axes((0.65, 0.48, 0.2, 0.03))
        self.minspeed_slider = Slider(
            self.ax_minspeed_slider,
            "Min",
            0,
            400,
            dragging=False,
            valinit=self.flock.min_speed,
            valstep=5,
        )
        self.maxspeed_slider = Slider(
            self.ax_maxspeed_slider,
            "Max",
            0,
            400,
            dragging=False,
            valinit=self.flock.max_speed,
            valstep=5,
            slidermin=self.minspeed_slider,
        )

        # View radii
        self.fig.text(0.75, 0.41, "Boid vision", ha="center", va="center", fontsize=12)
        self.ax_view_radius_slider = self.fig.add_axes((0.65, 0.36, 0.2, 0.03))
        self.ax_avoid_radius_slider = self.fig.add_axes((0.65, 0.33, 0.2, 0.03))
        self.view_radius_slider = Slider(
            self.ax_view_radius_slider,
            "View radius",
            1,
            500,
            valinit=self.flock.view_radius,
        )
        self.avoid_radius_slider = Slider(
            self.ax_avoid_radius_slider,
            "Avoidance radius",
            1,
            100,
            valinit=self.flock.avoid_radius,
            slidermax=self.view_radius_slider,
        )

        # Add or remove predators
        self.ax_sub_predator = self.fig.add_axes((0.65, 0.21, 0.08, 0.04))
        self.ax_add_predator = self.fig.add_axes((0.77, 0.21, 0.08, 0.04))
        self.sub_predator_btn = Button(self.ax_sub_predator, "-1 Predator")
        self.add_predator_btn = Button(self.ax_add_predator, "+1 Predator")

        # Add or remove axis lines
        self.ax_axes_btn = self.fig.add_axes((0.65, 0.16, 0.2, 0.04))
        self.axes_btn = Button(self.ax_axes_btn, "Show/hide axes")

        # Toggle rotation
        if self.ndim == 3:
            self.ax_rotation_btn = self.fig.add_axes((0.65, 0.11, 0.2, 0.04))
            self.rotation_btn = Button(self.ax_rotation_btn, "Toggle camera orbit")

        # Attach widget functionality
        # == Weights
        self.separation_slider.on_changed(self.set_separation_weight)
        self.alignment_slider.on_changed(self.set_alignment_weight)
        self.cohesion_slider.on_changed(self.set_cohesion_weight)
        self.flee_slider.on_changed(self.set_flee_weight)
        self.seek_slider.on_changed(self.set_seek_weight)
        # == Boid speed
        self.minspeed_slider.on_changed(self.set_minspeed)
        self.maxspeed_slider.on_changed(self.set_maxspeed)
        # == Boid vision
        self.view_radius_slider.on_changed(self.set_view_radius)
        self.avoid_radius_slider.on_changed(self.set_avoid_radius)
        # == Add/remove predator
        self.sub_predator_btn.on_clicked(self.remove_predator)
        self.add_predator_btn.on_clicked(self.add_predator)
        # == Axes control
        self.axes_btn.on_clicked(self.show_or_hide_axes)
        if self.ndim == 3:
            self.rotation_btn.on_clicked(self.toggle_camera_orbit)

    def set_minspeed(self, value):
        self.flock.min_speed = value

    def set_maxspeed(self, value):
        self.flock.max_speed = value

    def set_separation_weight(self, value):
        self.flock.weights.separation = value

    def set_alignment_weight(self, value):
        self.flock.weights.alignment = value

    def set_cohesion_weight(self, value):
        self.flock.weights.cohesion = value

    def set_flee_weight(self, value):
        self.flock.weights.flee = value

    def set_seek_weight(self, value):
        self.flock.weights.predator_seek = value

    def set_view_radius(self, value):
        self.flock.view_radius = value

    def set_avoid_radius(self, value):
        self.flock.avoid_radius = value

    def add_predator(self, value):
        self.flock.add_predator()

    def remove_predator(self, value):
        self.flock.remove_oldest_predator()

    def show_or_hide_axes(self, value):
        if self.show_axes:
            self.show_axes = False
            self.ax_plot.set_axis_off()
        else:
            self.show_axes = True
            self.ax_plot.set_axis_on()

    def toggle_camera_orbit(self, value):
        if self.camera_orbit_enabled:
            self.camera_orbit_enabled = False
        else:
            self.camera_orbit_enabled = True
