# RAWSim-O MVP - Python

🤖 A simplified Python implementation of **RAWSim-O** - Robotic Mobile Fulfillment System (RMFS) Simulator with real-time 2D/3D visualization.

> **Original Project:** [merschformann/RAWSim-O](https://github.com/merschformann/RAWSim-O) (C# .NET)
>
> This is a minimal viable product (MVP) version built with Python, focusing on core warehouse robot simulation with interactive visualization.

## 🎯 Features

✅ **Core Simulation Engine** - Discrete event-based simulation with time management

✅ **Robot/Bot Management** - Autonomous robots that navigate and carry pods

✅ **Pod & Item System** - Storage pods with inventory tracking

✅ **Waypoint Navigation** - Grid-based pathfinding system

✅ **Input/Output Stations** - Item receiving and order fulfillment stations

✅ **Real-time 2D Visualization** - Interactive Pygame-based top-down view

✅ **3D Visualization** - Matplotlib 3D warehouse visualization

✅ **Statistics Tracking** - Performance metrics and throughput analysis

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Run 2D Simulation (Interactive)

```bash
python main.py --mode 2d
```

### Run 3D Visualization

```bash
python main.py --mode 3d
```

### Run Both (Default)

```bash
python main.py
```

### Custom Configuration

```bash
python main.py --config configs/warehouse_config.json --duration 300
```

## 🎮 Controls (2D Mode)

- **SPACE** - Pause/Resume simulation
- **R** - Reset simulation
- **+/-** - Speed up/slow down
- **S** - Show/hide statistics
- **ESC** - Exit

## 🏗️ Project Structure

```
RAWSim-O-MVP-Python/
├── core/
│   ├── __init__.py
│   ├── instance.py          # Main simulation instance
│   ├── bot.py              # Robot/Bot implementation
│   ├── pod.py              # Storage pod
│   ├── waypoint.py         # Navigation waypoints
│   ├── station.py          # Input/Output stations
│   ├── simulator.py        # Simulation executor
│   └── pathfinding.py      # A* pathfinding algorithm
├── visualization/
│   ├── __init__.py
│   ├── renderer_2d.py      # Pygame 2D renderer
│   └── renderer_3d.py      # Matplotlib 3D renderer
├── configs/
│   └── warehouse_config.json  # Default configuration
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## ⚙️ Configuration

Edit `configs/warehouse_config.json` to customize:

```json
{
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
```

## 📊 Example Output

```
=== RAWSim-O MVP - Warehouse Robot Simulation ===
Starting simulation...

Warehouse Layout: 30x20 grid
Robots: 8
Pods: 40
Input Stations: 2
Output Stations: 2

>>> Warming up (10.0s)...
>>> Warmup complete!
>>> Running simulation (300.0s)...

=== Simulation Statistics ===
Total Time: 300.00s
Orders Completed: 156
Items Picked: 487
Average Robot Utilization: 73.2%
Average Order Completion Time: 18.4s
```

## 🎥 Demo

### 2D View (Pygame)

- **Green rectangles**: Robots (idle)
- **Red rectangles**: Robots carrying pods
- **Blue circles**: Pods at storage
- **Yellow squares**: Input stations
- **Purple squares**: Output stations
- **Gray dots**: Waypoints

### 3D View (Matplotlib)

- Interactive 3D warehouse visualization
- Rotate/zoom with mouse
- Real-time robot and pod positions

## 🔬 How It Works

1. **Warehouse Generation**: Creates a grid-based warehouse with waypoints, storage locations, and stations
2. **Robot Initialization**: Spawns robots at starting positions
3. **Order Generation**: Creates random orders for items
4. **Task Assignment**: Assigns robots to fetch pods containing requested items
5. **Pathfinding**: Robots use A* algorithm to navigate collision-free
6. **Order Fulfillment**: Robots deliver pods to output stations for picking
7. **Pod Return**: After picking, robots return pods to storage

## 📝 Differences from Original RAWSim-O

| Feature | Original (C#) | This MVP (Python) |
|---------|--------------|-------------------|
| Language | C# .NET 6.0 | Python 3.8+ |
| Visualization | WPF/Helix 3D | Pygame + Matplotlib |
| Pathfinding | Multi-Agent (WHCA*, CBS) | Simple A* |
| Controllers | Pluggable framework | Basic greedy assignment |
| Instance Generation | XML-based layouts | JSON configuration |
| Hardware Integration | Supported | Not included |
| Scale | 1000+ robots | Optimized for <50 robots |

## 🛠️ Development

### Run Tests

```bash
python -m pytest tests/
```

### Add New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📚 References

- **Original Paper**: Merschformann et al., "RAWSim-O: A Simulation Framework for Robotic Mobile Fulfillment Systems", Logistics Research (2018)
- **Original Repository**: https://github.com/merschformann/RAWSim-O

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Credits

This MVP is inspired by the original RAWSim-O project by Marius Merschformann and contributors. Special thanks to the RAWSim-O team for their excellent research and open-source contribution to warehouse automation simulation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ for warehouse automation enthusiasts**