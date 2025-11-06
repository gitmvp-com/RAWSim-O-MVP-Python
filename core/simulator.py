"""
SimulationExecutor - Simulation Runner

Executes the simulation loop.
"""

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import Instance


class SimulationExecutor:
    """Executes simulation instances."""

    @staticmethod
    def execute(instance: 'Instance'):
        """Execute a simulation instance (headless mode)."""
        warmup_time = instance.config['simulation'].get('warmup_time', 10)
        duration = instance.config['simulation'].get('duration', 300)
        time_step = instance.config['simulation'].get('time_step', 0.1)

        print(f"\n>>> Warming up ({warmup_time}s)...")
        instance.running = True
        start_time = time.time()

        # Warmup phase
        while instance.current_time < warmup_time:
            instance.update(time_step)
            time.sleep(0.01)  # Prevent busy waiting

        print(">>> Warmup complete!")
        print(f">>> Running simulation ({duration}s)...\n")

        # Reset statistics after warmup
        instance.reset_statistics()
        sim_start_time = instance.current_time

        # Main simulation loop
        try:
            while instance.current_time - sim_start_time < duration:
                instance.update(time_step)
                time.sleep(0.01)  # Prevent busy waiting

                # Print progress every 60 seconds
                if int(instance.current_time) % 60 == 0 and instance.current_time > 0:
                    elapsed = instance.current_time - sim_start_time
                    print(f"Progress: {elapsed:.0f}s / {duration}s - Orders: {instance.stats['orders_completed']}")

        except KeyboardInterrupt:
            print("\nSimulation interrupted by user.")

        instance.running = False
        instance.stats['end_time'] = time.time()

        # Print final statistics
        instance.print_statistics()