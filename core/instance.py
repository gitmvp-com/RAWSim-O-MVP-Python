"""
Instance - Main Simulation Instance

Represents a complete warehouse simulation instance with all elements.
"""

import random
from typing import List, Dict, Optional
import time

from .bot import Bot
from .pod import Pod
from .waypoint import Waypoint
from .station import InputStation, OutputStation


class Instance:
    """Main simulation instance containing all warehouse elements."""

    def __init__(self, config: dict):
        """Initialize the simulation instance."""
        self.config = config
        self.name = "RAWSim-O-MVP"

        # Core elements
        self.bots: List[Bot] = []
        self.pods: List[Pod] = []
        self.waypoints: List[Waypoint] = []
        self.input_stations: List[InputStation] = []
        self.output_stations: List[OutputStation] = []

        # Waypoint grid for easy access
        self.waypoint_grid: Dict[tuple, Waypoint] = {}

        # Simulation state
        self.current_time = 0.0
        self.time_step = config['simulation'].get('time_step', 0.1)
        self.running = False
        self.paused = False

        # Statistics
        self.stats = {
            'orders_completed': 0,
            'items_picked': 0,
            'total_distance_traveled': 0.0,
            'bot_busy_time': 0.0,
            'bot_idle_time': 0.0,
            'start_time': None,
            'end_time': None
        }

        # Pending orders (simplified)
        self.pending_orders = []
        self.active_tasks = {}

    def generate_layout(self):
        """Generate warehouse layout from configuration."""
        warehouse_cfg = self.config['warehouse']
        width = warehouse_cfg['width']
        height = warehouse_cfg['height']

        print("Generating waypoint grid...")
        # Create waypoint grid
        wp_id = 0
        for y in range(height):
            for x in range(width):
                wp = Waypoint(wp_id, x, y, self)
                self.waypoints.append(wp)
                self.waypoint_grid[(x, y)] = wp
                wp_id += 1

        # Connect waypoints (4-directional)
        for wp in self.waypoints:
            x, y = wp.x, wp.y
            # Right
            if (x + 1, y) in self.waypoint_grid:
                wp.add_path(self.waypoint_grid[(x + 1, y)])
            # Down
            if (x, y + 1) in self.waypoint_grid:
                wp.add_path(self.waypoint_grid[(x, y + 1)])
            # Left
            if (x - 1, y) in self.waypoint_grid:
                wp.add_path(self.waypoint_grid[(x - 1, y)])
            # Up
            if (x, y - 1) in self.waypoint_grid:
                wp.add_path(self.waypoint_grid[(x, y - 1)])

        print("Placing stations...")
        # Place input stations (top of warehouse)
        station_cfg = self.config['stations']
        input_spacing = width // (station_cfg['input_count'] + 1)
        for i in range(station_cfg['input_count']):
            x = input_spacing * (i + 1)
            y = 0
            wp = self.waypoint_grid[(x, y)]
            station = InputStation(i, wp, self)
            self.input_stations.append(station)
            wp.input_station = station

        # Place output stations (bottom of warehouse)
        output_spacing = width // (station_cfg['output_count'] + 1)
        for i in range(station_cfg['output_count']):
            x = output_spacing * (i + 1)
            y = height - 1
            wp = self.waypoint_grid[(x, y)]
            station = OutputStation(i, wp, self)
            self.output_stations.append(station)
            wp.output_station = station

        print("Creating pod storage locations...")
        # Mark pod storage locations (middle section)
        storage_rows = warehouse_cfg.get('pod_storage_rows', 5)
        storage_y_start = height // 2 - storage_rows // 2
        storage_y_end = storage_y_start + storage_rows

        for y in range(storage_y_start, storage_y_end):
            for x in range(2, width - 2):  # Leave aisles on sides
                if x % 3 != 0:  # Leave aisles every 3 columns
                    wp = self.waypoint_grid[(x, y)]
                    wp.pod_storage_location = True

        print("Initializing pods...")
        # Create pods and place them at storage locations
        pod_cfg = self.config['pods']
        storage_waypoints = [wp for wp in self.waypoints if wp.pod_storage_location]
        random.shuffle(storage_waypoints)

        for i in range(min(pod_cfg['count'], len(storage_waypoints))):
            pod = Pod(i, pod_cfg['capacity'], self)
            wp = storage_waypoints[i]
            pod.waypoint = wp
            wp.pod = pod
            pod.x = wp.x
            pod.y = wp.y
            # Add some random items to pods
            for _ in range(random.randint(5, 20)):
                pod.add_item(f"item_{random.randint(1, 50)}")
            self.pods.append(pod)

        print("Spawning robots...")
        # Create robots and place them at random free waypoints
        robot_cfg = self.config['robots']
        free_waypoints = [wp for wp in self.waypoints if not wp.pod and not wp.input_station and not wp.output_station]
        random.shuffle(free_waypoints)

        for i in range(min(robot_cfg['count'], len(free_waypoints))):
            bot = Bot(i, robot_cfg['speed'], self)
            wp = free_waypoints[i]
            bot.current_waypoint = wp
            bot.x = wp.x
            bot.y = wp.y
            self.bots.append(bot)

        print(f"Layout generation complete! ({len(self.waypoints)} waypoints, {len(self.pods)} pods, {len(self.bots)} robots)")

    def update(self, delta_time: float):
        """Update simulation state."""
        if self.paused:
            return

        self.current_time += delta_time

        # Update all bots
        for bot in self.bots:
            bot.update(delta_time)

        # Simple order generation (random)
        if random.random() < 0.05:  # 5% chance per update
            self.generate_random_order()

        # Assign tasks to idle bots
        self.assign_tasks()

    def generate_random_order(self):
        """Generate a random order for testing."""
        items = [f"item_{random.randint(1, 50)}" for _ in range(random.randint(1, 3))]
        order = {
            'id': len(self.pending_orders),
            'items': items,
            'station': random.choice(self.output_stations) if self.output_stations else None
        }
        self.pending_orders.append(order)

    def assign_tasks(self):
        """Assign pending orders to idle robots."""
        idle_bots = [bot for bot in self.bots if bot.state == 'idle']

        for bot in idle_bots:
            if not self.pending_orders:
                break

            order = self.pending_orders.pop(0)
            # Find a pod containing requested items
            suitable_pod = self.find_pod_with_items(order['items'])

            if suitable_pod and order['station']:
                # Assign task to bot
                bot.assign_task('fetch_pod', suitable_pod, order['station'])
                self.active_tasks[bot.id] = order

    def find_pod_with_items(self, items: List[str]) -> Optional[Pod]:
        """Find a pod containing at least one of the requested items."""
        for pod in self.pods:
            if not pod.in_use:
                for item in items:
                    if item in pod.items:
                        return pod
        return None

    def complete_order(self, bot: Bot):
        """Mark an order as completed."""
        if bot.id in self.active_tasks:
            order = self.active_tasks.pop(bot.id)
            self.stats['orders_completed'] += 1
            self.stats['items_picked'] += len(order['items'])

    def reset_statistics(self):
        """Reset all statistics."""
        self.stats = {
            'orders_completed': 0,
            'items_picked': 0,
            'total_distance_traveled': 0.0,
            'bot_busy_time': 0.0,
            'bot_idle_time': 0.0,
            'start_time': time.time(),
            'end_time': None
        }

    def print_statistics(self):
        """Print current statistics."""
        print("\n" + "="*60)
        print("=== Simulation Statistics ===")
        print("="*60)
        print(f"Simulation Time: {self.current_time:.2f}s")
        print(f"Orders Completed: {self.stats['orders_completed']}")
        print(f"Items Picked: {self.stats['items_picked']}")
        print(f"Total Distance Traveled: {self.stats['total_distance_traveled']:.2f} units")

        if self.bots:
            total_time = sum(bot.busy_time + bot.idle_time for bot in self.bots)
            busy_time = sum(bot.busy_time for bot in self.bots)
            utilization = (busy_time / total_time * 100) if total_time > 0 else 0
            print(f"Average Robot Utilization: {utilization:.1f}%")

        print("="*60)