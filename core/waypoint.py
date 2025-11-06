"""
Waypoint - Navigation Graph Node

Represents a waypoint in the warehouse navigation graph.
"""

from typing import List, Optional, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from .instance import Instance
    from .pod import Pod
    from .station import InputStation, OutputStation


class Waypoint:
    """Waypoint in the warehouse navigation graph."""

    def __init__(self, waypoint_id: int, x: float, y: float, instance: 'Instance'):
        """Initialize a waypoint."""
        self.id = waypoint_id
        self.x = x
        self.y = y
        self.instance = instance

        # Connections
        self.paths: List['Waypoint'] = []
        self.path_distances: dict = {}  # {waypoint: distance}

        # Elements at this waypoint
        self.pod: Optional['Pod'] = None
        self.input_station: Optional['InputStation'] = None
        self.output_station: Optional['OutputStation'] = None

        # Flags
        self.pod_storage_location = False
        self.is_queue = False

        # Bot tracking
        self.bots_approaching = set()
        self.bots_leaving = set()

    def add_path(self, other: 'Waypoint'):
        """Add a directed path to another waypoint."""
        if other not in self.paths:
            self.paths.append(other)
            distance = self.get_distance(other)
            self.path_distances[other] = distance

    def get_distance(self, other: 'Waypoint') -> float:
        """Calculate Euclidean distance to another waypoint."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def is_accessible(self, other: 'Waypoint') -> bool:
        """Check if another waypoint is directly accessible."""
        return other in self.paths

    def is_occupied(self) -> bool:
        """Check if waypoint is occupied by a pod or station."""
        return self.pod is not None or self.input_station is not None or self.output_station is not None

    def __repr__(self):
        return f"Waypoint{self.id}({self.x}, {self.y})"