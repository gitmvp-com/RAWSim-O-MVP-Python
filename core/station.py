"""
Station - Input/Output Stations

Represents input and output stations for items.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .waypoint import Waypoint


class InputStation:
    """Input station where items enter the warehouse."""

    def __init__(self, station_id: int, waypoint: 'Waypoint', instance: 'Instance'):
        """Initialize an input station."""
        self.id = station_id
        self.waypoint = waypoint
        self.instance = instance

        # Statistics
        self.bundles_stored = 0
        self.items_stored = 0

    def __repr__(self):
        return f"InputStation{self.id}"


class OutputStation:
    """Output station where orders are fulfilled."""

    def __init__(self, station_id: int, waypoint: 'Waypoint', instance: 'Instance'):
        """Initialize an output station."""
        self.id = station_id
        self.waypoint = waypoint
        self.instance = instance

        # Statistics
        self.orders_completed = 0
        self.items_picked = 0

    def __repr__(self):
        return f"OutputStation{self.id}"