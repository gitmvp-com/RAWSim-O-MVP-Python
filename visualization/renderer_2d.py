"""
Renderer2D - Pygame 2D Visualization

Real-time interactive 2D visualization using Pygame.
"""

import pygame
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.instance import Instance


class Renderer2D:
    """2D renderer using Pygame."""

    def __init__(self, instance: 'Instance', cell_size: int = 25):
        """Initialize 2D renderer."""
        self.instance = instance
        self.cell_size = cell_size

        # Calculate window size
        width = instance.config['warehouse']['width']
        height = instance.config['warehouse']['height']
        self.window_width = width * cell_size + 300  # Extra space for UI
        self.window_height = height * cell_size + 100

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("RAWSim-O MVP - 2D View")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # Colors
        self.colors = {
            'background': (20, 20, 30),
            'grid': (50, 50, 60),
            'waypoint': (80, 80, 90),
            'storage': (60, 80, 100),
            'bot_idle': (100, 200, 100),
            'bot_busy': (200, 100, 100),
            'pod': (100, 150, 255),
            'input_station': (255, 200, 100),
            'output_station': (200, 100, 255),
            'text': (255, 255, 255),
            'path': (255, 255, 100)
        }

        # UI state
        self.show_stats = True
        self.speed_multiplier = 1.0
        self.offset_x = 50
        self.offset_y = 50

    def run(self):
        """Main rendering loop."""
        self.instance.running = True
        running = True

        while running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS, delta time in seconds

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self.handle_keypress(event.key)

            # Update simulation
            if not self.instance.paused:
                self.instance.update(dt * self.speed_multiplier)

            # Render
            self.render()

            pygame.display.flip()

        self.instance.running = False
        pygame.quit()

    def handle_keypress(self, key) -> bool:
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            return False
        elif key == pygame.K_SPACE:
            self.instance.paused = not self.instance.paused
        elif key == pygame.K_r:
            # Reset simulation
            self.instance.current_time = 0
            self.instance.reset_statistics()
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.speed_multiplier = min(self.speed_multiplier * 2, 16)
        elif key == pygame.K_MINUS:
            self.speed_multiplier = max(self.speed_multiplier / 2, 0.25)
        elif key == pygame.K_s:
            self.show_stats = not self.show_stats
        return True

    def render(self):
        """Render the warehouse."""
        self.screen.fill(self.colors['background'])

        # Draw grid and waypoints
        self.draw_waypoints()

        # Draw stations
        self.draw_stations()

        # Draw pods
        self.draw_pods()

        # Draw bots
        self.draw_bots()

        # Draw UI
        self.draw_ui()

    def draw_waypoints(self):
        """Draw waypoint grid."""
        for wp in self.instance.waypoints:
            x = self.offset_x + wp.x * self.cell_size
            y = self.offset_y + wp.y * self.cell_size

            # Draw storage locations differently
            if wp.pod_storage_location:
                color = self.colors['storage']
                pygame.draw.rect(self.screen, color, (x - 3, y - 3, 6, 6))
            else:
                color = self.colors['waypoint']
                pygame.draw.circle(self.screen, color, (x, y), 2)

    def draw_stations(self):
        """Draw input and output stations."""
        # Input stations
        for station in self.instance.input_stations:
            wp = station.waypoint
            x = self.offset_x + wp.x * self.cell_size
            y = self.offset_y + wp.y * self.cell_size
            pygame.draw.rect(self.screen, self.colors['input_station'], (x - 8, y - 8, 16, 16))
            text = self.small_font.render(f"I{station.id}", True, self.colors['text'])
            self.screen.blit(text, (x - 8, y - 20))

        # Output stations
        for station in self.instance.output_stations:
            wp = station.waypoint
            x = self.offset_x + wp.x * self.cell_size
            y = self.offset_y + wp.y * self.cell_size
            pygame.draw.rect(self.screen, self.colors['output_station'], (x - 8, y - 8, 16, 16))
            text = self.small_font.render(f"O{station.id}", True, self.colors['text'])
            self.screen.blit(text, (x - 8, y + 10))

    def draw_pods(self):
        """Draw pods."""
        for pod in self.instance.pods:
            if not pod.in_use:  # Don't draw pods being carried
                x = self.offset_x + pod.x * self.cell_size
                y = self.offset_y + pod.y * self.cell_size
                pygame.draw.circle(self.screen, self.colors['pod'], (int(x), int(y)), 6)

    def draw_bots(self):
        """Draw robots."""
        for bot in self.instance.bots:
            x = self.offset_x + bot.x * self.cell_size
            y = self.offset_y + bot.y * self.cell_size

            # Color based on state
            color = self.colors['bot_busy'] if bot.carrying_pod else self.colors['bot_idle']
            pygame.draw.rect(self.screen, color, (x - 6, y - 6, 12, 12))

            # Draw carried pod
            if bot.carrying_pod:
                pygame.draw.circle(self.screen, self.colors['pod'], (int(x), int(y)), 4)

    def draw_ui(self):
        """Draw UI overlay."""
        ui_x = self.offset_x + self.instance.config['warehouse']['width'] * self.cell_size + 20
        y = 20

        # Title
        title = self.font.render("RAWSim-O MVP", True, self.colors['text'])
        self.screen.blit(title, (ui_x, y))
        y += 40

        # Time
        time_text = self.small_font.render(f"Time: {self.instance.current_time:.1f}s", True, self.colors['text'])
        self.screen.blit(time_text, (ui_x, y))
        y += 25

        # Speed
        speed_text = self.small_font.render(f"Speed: {self.speed_multiplier}x", True, self.colors['text'])
        self.screen.blit(speed_text, (ui_x, y))
        y += 25

        # Status
        status = "PAUSED" if self.instance.paused else "RUNNING"
        status_color = (255, 200, 100) if self.instance.paused else (100, 255, 100)
        status_text = self.small_font.render(status, True, status_color)
        self.screen.blit(status_text, (ui_x, y))
        y += 40

        # Statistics
        if self.show_stats:
            stats_title = self.font.render("Statistics", True, self.colors['text'])
            self.screen.blit(stats_title, (ui_x, y))
            y += 30

            stats = [
                f"Orders: {self.instance.stats['orders_completed']}",
                f"Items: {self.instance.stats['items_picked']}",
                f"Distance: {self.instance.stats['total_distance_traveled']:.1f}",
                f"Robots: {len(self.instance.bots)}",
                f"Pods: {len(self.instance.pods)}",
            ]

            for stat in stats:
                text = self.small_font.render(stat, True, self.colors['text'])
                self.screen.blit(text, (ui_x, y))
                y += 20

        # Controls
        y = self.window_height - 120
        controls_title = self.small_font.render("Controls:", True, self.colors['text'])
        self.screen.blit(controls_title, (ui_x, y))
        y += 20

        controls = [
            "SPACE: Pause",
            "R: Reset",
            "+/-: Speed",
            "S: Stats",
        ]

        for control in controls:
            text = self.small_font.render(control, True, (180, 180, 180))
            self.screen.blit(text, (ui_x, y))
            y += 18