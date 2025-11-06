"""
Pathfinding - A* Algorithm Implementation

Implements A* pathfinding for robot navigation.
"""

import heapq
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .waypoint import Waypoint


class AStar:
    """A* pathfinding algorithm."""

    def __init__(self, instance: 'Instance'):
        """Initialize pathfinder."""
        self.instance = instance

    def find_path(self, start: 'Waypoint', goal: 'Waypoint') -> List['Waypoint']:
        """Find shortest path from start to goal using A*."""
        if start == goal:
            return [start]

        # Priority queue: (f_score, waypoint)
        open_set = [(0, start)]
        came_from = {}

        # g_score: cost from start to waypoint
        g_score = {wp: float('inf') for wp in self.instance.waypoints}
        g_score[start] = 0

        # f_score: estimated total cost from start to goal through waypoint
        f_score = {wp: float('inf') for wp in self.instance.waypoints}
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in current.paths:
                # Check if neighbor is accessible (not blocked)
                if self.is_blocked(neighbor, goal):
                    continue

                tentative_g_score = g_score[current] + current.get_distance(neighbor)

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    # Add to open set if not already there
                    if not any(neighbor == wp for _, wp in open_set):
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # No path found
        return []

    def heuristic(self, wp1: 'Waypoint', wp2: 'Waypoint') -> float:
        """Manhattan distance heuristic."""
        return abs(wp1.x - wp2.x) + abs(wp1.y - wp2.y)

    def is_blocked(self, waypoint: 'Waypoint', goal: 'Waypoint') -> bool:
        """Check if waypoint is blocked (has pod, unless it's the goal)."""
        if waypoint == goal:
            return False
        # Waypoint is blocked if it has a pod that's not being carried
        return waypoint.pod is not None and not waypoint.pod.in_use

    def reconstruct_path(self, came_from: dict, current: 'Waypoint') -> List['Waypoint']:
        """Reconstruct path from came_from map."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path