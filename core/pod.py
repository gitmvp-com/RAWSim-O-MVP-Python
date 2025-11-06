"""
Pod - Storage Pod

Represents a storage pod that can hold items.
"""

from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance
    from .waypoint import Waypoint
    from .bot import Bot


class Pod:
    """Storage pod containing items."""

    def __init__(self, pod_id: int, capacity: float, instance: 'Instance'):
        """Initialize a pod."""
        self.id = pod_id
        self.capacity = capacity
        self.instance = instance

        # Position
        self.x = 0.0
        self.y = 0.0
        self.waypoint: Optional['Waypoint'] = None

        # State
        self.in_use = False
        self.bot: Optional['Bot'] = None

        # Contents (simplified - just item names and counts)
        self.items: Dict[str, int] = {}
        self.capacity_used = 0.0

        # Statistics
        self.items_handled = 0
        self.bundles_handled = 0

    def add_item(self, item_name: str, weight: float = 1.0, count: int = 1):
        """Add an item to the pod."""
        if self.capacity_used + weight * count <= self.capacity:
            if item_name in self.items:
                self.items[item_name] += count
            else:
                self.items[item_name] = count
            self.capacity_used += weight * count
            self.bundles_handled += 1
            return True
        return False

    def remove_item(self, item_name: str, weight: float = 1.0, count: int = 1):
        """Remove an item from the pod."""
        if item_name in self.items and self.items[item_name] >= count:
            self.items[item_name] -= count
            if self.items[item_name] <= 0:
                del self.items[item_name]
            self.capacity_used -= weight * count
            self.items_handled += count
            return True
        return False

    def contains(self, item_name: str) -> bool:
        """Check if pod contains an item."""
        return item_name in self.items and self.items[item_name] > 0

    def get_capacity_utilization(self) -> float:
        """Get capacity utilization as a percentage."""
        return (self.capacity_used / self.capacity) * 100 if self.capacity > 0 else 0

    def __repr__(self):
        return f"Pod{self.id}({self.get_capacity_utilization():.1f}%)"