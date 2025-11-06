#!/usr/bin/env python3
"""
RAWSim-O MVP - Main Entry Point

A simplified Python implementation of RAWSim-O - Robotic Mobile Fulfillment System Simulator
with real-time 2D/3D visualization.

Based on: merschformann/RAWSim-O (C# .NET)
"""

import argparse
import json
import sys
from pathlib import Path

from core.instance import Instance
from core.simulator import SimulationExecutor
from visualization.renderer_2d import Renderer2D
from visualization.renderer_3d import Renderer3D


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Config file '{config_path}' not found. Using defaults.")
        return get_default_config()
    except json.JSONDecodeError as e:
        print(f"Error parsing config file: {e}")
        sys.exit(1)


def get_default_config() -> dict:
    """Return default configuration."""
    return {
        "warehouse": {
            "width": 30,
            "height": 20,
            "pod_storage_rows": 5
        },
        "robots": {
            "count": 8,
            "speed": 2.0,
            "capacity": 1
        },
        "pods": {
            "count": 40,
            "capacity": 100.0
        },
        "stations": {
            "input_count": 2,
            "output_count": 2
        },
        "simulation": {
            "duration": 300,
            "warmup_time": 10,
            "time_step": 0.1
        }
    }


def print_banner():
    """Print welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                  RAWSim-O MVP - Python                    ║
║         Robotic Mobile Fulfillment System Simulator       ║
║                                                           ║
║  Based on: merschformann/RAWSim-O (C# .NET)              ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main application entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='RAWSim-O MVP - Warehouse Robot Simulation'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='configs/warehouse_config.json',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=['2d', '3d', 'both'],
        default='both',
        help='Visualization mode (2d, 3d, or both)'
    )
    parser.add_argument(
        '--duration',
        type=float,
        help='Simulation duration in seconds (overrides config)'
    )
    parser.add_argument(
        '--no-gui',
        action='store_true',
        help='Run simulation without visualization (headless mode)'
    )

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Load configuration
    print(f"Loading configuration from: {args.config}")
    config = load_config(args.config)

    # Override duration if specified
    if args.duration:
        config['simulation']['duration'] = args.duration

    # Create simulation instance
    print("\nInitializing simulation instance...")
    instance = Instance(config)
    instance.generate_layout()

    print(f"\nWarehouse Layout: {config['warehouse']['width']}x{config['warehouse']['height']} grid")
    print(f"Robots: {config['robots']['count']}")
    print(f"Pods: {config['pods']['count']}")
    print(f"Input Stations: {config['stations']['input_count']}")
    print(f"Output Stations: {config['stations']['output_count']}")

    # Run simulation
    if args.no_gui:
        # Headless mode - no visualization
        print("\nRunning in headless mode (no visualization)...")
        SimulationExecutor.execute(instance)
    else:
        # With visualization
        if args.mode == '2d' or args.mode == 'both':
            print("\nStarting 2D visualization...")
            print("\nControls:")
            print("  SPACE - Pause/Resume")
            print("  R - Reset simulation")
            print("  +/- - Speed up/slow down")
            print("  S - Show/hide statistics")
            print("  ESC - Exit\n")
            renderer = Renderer2D(instance)
            renderer.run()

        if args.mode == '3d':
            print("\nStarting 3D visualization...")
            renderer = Renderer3D(instance)
            renderer.run()

    print("\n" + "="*60)
    print("Simulation completed!")
    print("="*60)


if __name__ == "__main__":
    main()