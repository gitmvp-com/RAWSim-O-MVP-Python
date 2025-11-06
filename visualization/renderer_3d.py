"""
Renderer3D - Matplotlib 3D Visualization

Static/animated 3D visualization using Matplotlib.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.instance import Instance


class Renderer3D:
    """3D renderer using Matplotlib."""

    def __init__(self, instance: 'Instance'):
        """Initialize 3D renderer."""
        self.instance = instance
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

    def run(self, animate: bool = False):
        """Run 3D visualization."""
        if animate:
            # Animated mode (not implemented in this MVP)
            print("Animated 3D mode not implemented. Showing static view.")

        self.render_static()
        plt.show()

    def render_static(self):
        """Render a static 3D view of the warehouse."""
        self.ax.clear()

        # Set labels and title
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('RAWSim-O MVP - 3D Warehouse View')

        # Draw waypoints as a grid at z=0
        waypoint_x = [wp.x for wp in self.instance.waypoints]
        waypoint_y = [wp.y for wp in self.instance.waypoints]
        waypoint_z = [0] * len(self.instance.waypoints)
        self.ax.scatter(waypoint_x, waypoint_y, waypoint_z, c='gray', marker='.', s=10, alpha=0.3)

        # Draw storage locations
        storage_wps = [wp for wp in self.instance.waypoints if wp.pod_storage_location]
        if storage_wps:
            storage_x = [wp.x for wp in storage_wps]
            storage_y = [wp.y for wp in storage_wps]
            storage_z = [0] * len(storage_wps)
            self.ax.scatter(storage_x, storage_y, storage_z, c='lightblue', marker='s', s=50, alpha=0.5)

        # Draw input stations
        for station in self.instance.input_stations:
            wp = station.waypoint
            self.ax.scatter([wp.x], [wp.y], [0], c='yellow', marker='^', s=200, label=f'Input {station.id}')

        # Draw output stations
        for station in self.instance.output_stations:
            wp = station.waypoint
            self.ax.scatter([wp.x], [wp.y], [0], c='purple', marker='v', s=200, label=f'Output {station.id}')

        # Draw pods (at height 0.5)
        pod_x = [pod.x for pod in self.instance.pods if not pod.in_use]
        pod_y = [pod.y for pod in self.instance.pods if not pod.in_use]
        pod_z = [0.5] * len([pod for pod in self.instance.pods if not pod.in_use])
        if pod_x:
            self.ax.scatter(pod_x, pod_y, pod_z, c='blue', marker='o', s=100, alpha=0.7, label='Pods')

        # Draw bots (at height 1.0)
        bot_x = [bot.x for bot in self.instance.bots]
        bot_y = [bot.y for bot in self.instance.bots]
        bot_z = [1.0] * len(self.instance.bots)

        # Color based on carrying pod
        bot_colors = ['red' if bot.carrying_pod else 'green' for bot in self.instance.bots]
        if bot_x:
            for i, (x, y, z, color) in enumerate(zip(bot_x, bot_y, bot_z, bot_colors)):
                self.ax.scatter([x], [y], [z], c=color, marker='s', s=150, alpha=0.9,
                              label=f'Bot {i} (carrying)' if color == 'red' else f'Bot {i} (idle)' if i == 0 else '')

        # Set axis limits
        width = self.instance.config['warehouse']['width']
        height = self.instance.config['warehouse']['height']
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.set_zlim(0, 2)

        # Add legend (but limit entries)
        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys(), loc='upper left')

        # Set viewing angle
        self.ax.view_init(elev=30, azim=45)