"""
Bot - Autonomous Warehouse Robot

Implements robot movement, pathfinding, and task execution.
"""

import math
from typing import Optional, List, TYPE_CHECKING

from .pathfinding import AStar

if TYPE_CHECKING:
    from .instance import Instance
    from .waypoint import Waypoint
    from .pod import Pod
    from .station import OutputStation


class Bot:
    """Autonomous warehouse robot."""

    def __init__(self, bot_id: int, speed: float, instance: 'Instance'):
        """Initialize a bot."""
        self.id = bot_id
        self.speed = speed
        self.instance = instance

        # Position
        self.x = 0.0
        self.y = 0.0
        self.current_waypoint: Optional['Waypoint'] = None

        # Navigation
        self.path: List['Waypoint'] = []
        self.path_index = 0
        self.target_x = 0.0
        self.target_y = 0.0

        # State
        self.state = 'idle'  # idle, moving, picking, dropping
        self.carrying_pod: Optional['Pod'] = None

        # Task
        self.current_task = None
        self.target_pod: Optional['Pod'] = None
        self.target_station: Optional['OutputStation'] = None

        # Statistics
        self.busy_time = 0.0
        self.idle_time = 0.0
        self.distance_traveled = 0.0

    def assign_task(self, task_type: str, pod: 'Pod', station: 'OutputStation'):
        """Assign a task to this bot."""
        self.current_task = task_type
        self.target_pod = pod
        self.target_station = station
        self.state = 'moving'

        # Calculate path to pod
        if pod.waypoint:
            self.calculate_path(pod.waypoint)

    def calculate_path(self, destination: 'Waypoint'):
        """Calculate A* path to destination."""
        if self.current_waypoint:
            pathfinder = AStar(self.instance)
            self.path = pathfinder.find_path(self.current_waypoint, destination)
            self.path_index = 0

            if self.path:
                # Set first target
                next_wp = self.path[self.path_index]
                self.target_x = next_wp.x
                self.target_y = next_wp.y

    def update(self, delta_time: float):
        """Update bot state."""
        if self.state == 'idle':
            self.idle_time += delta_time
            return

        if self.state == 'moving':
            self.busy_time += delta_time
            self.move(delta_time)

    def move(self, delta_time: float):
        """Move bot towards target."""
        if not self.path or self.path_index >= len(self.path):
            self.on_destination_reached()
            return

        # Calculate distance to target waypoint
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < 0.1:  # Reached waypoint
            # Snap to waypoint
            self.x = self.target_x
            self.y = self.target_y
            self.current_waypoint = self.path[self.path_index]

            # Move to next waypoint
            self.path_index += 1
            if self.path_index < len(self.path):
                next_wp = self.path[self.path_index]
                self.target_x = next_wp.x
                self.target_y = next_wp.y
            else:
                self.on_destination_reached()
        else:
            # Move towards target
            move_distance = self.speed * delta_time
            if move_distance > distance:
                move_distance = distance

            # Normalize direction and move
            self.x += (dx / distance) * move_distance
            self.y += (dy / distance) * move_distance

            # Update statistics
            self.distance_traveled += move_distance
            self.instance.stats['total_distance_traveled'] += move_distance

            # Update pod position if carrying
            if self.carrying_pod:
                self.carrying_pod.x = self.x
                self.carrying_pod.y = self.y

    def on_destination_reached(self):
        """Handle reaching destination waypoint."""
        if self.current_task == 'fetch_pod':
            if self.target_pod and not self.carrying_pod:
                # Pick up pod
                self.pick_up_pod(self.target_pod)
                # Navigate to station
                if self.target_station:
                    self.calculate_path(self.target_station.waypoint)
            elif self.carrying_pod and self.target_station:
                # Drop off pod at station
                self.drop_pod()
                # Complete order
                self.instance.complete_order(self)
                # Return pod to storage
                if self.target_pod and self.target_pod.waypoint:
                    self.pick_up_pod(self.target_pod)
                    self.calculate_path(self.target_pod.waypoint)
                    self.current_task = 'return_pod'
            else:
                # Task complete
                self.complete_task()
        elif self.current_task == 'return_pod':
            if self.carrying_pod:
                self.drop_pod()
            self.complete_task()

    def pick_up_pod(self, pod: 'Pod'):
        """Pick up a pod."""
        self.carrying_pod = pod
        pod.in_use = True
        pod.bot = self
        if pod.waypoint:
            pod.waypoint.pod = None
            pod.waypoint = None

    def drop_pod(self):
        """Drop the carried pod at current location."""
        if self.carrying_pod and self.current_waypoint:
            self.carrying_pod.waypoint = self.current_waypoint
            self.current_waypoint.pod = self.carrying_pod
            self.carrying_pod.x = self.current_waypoint.x
            self.carrying_pod.y = self.current_waypoint.y
            self.carrying_pod.in_use = False
            self.carrying_pod.bot = None
            self.carrying_pod = None

    def complete_task(self):
        """Complete current task and return to idle."""
        self.current_task = None
        self.target_pod = None
        self.target_station = None
        self.state = 'idle'
        self.path = []
        self.path_index = 0