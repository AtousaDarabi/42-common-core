"""Command-line entry point for the Fly-in project."""

import argparse
import sys

from fly_in.parser import MapParseError, MapParser
from fly_in.pathfinder import Pathfinder
from fly_in.simulation import Simulation
from fly_in.visualizer import TerminalVisualizer


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(description="Route drones through a map")
    parser.add_argument("map_file", help="path to a Fly-in map file")
    parser.add_argument(
        "--plain", action="store_true", help="disable terminal colors"
    )
    parser.add_argument(
        "--stats", action="store_true", help="BONUS: print performance metrics"
    )
    parser.add_argument(
        "--routes",
        action="store_true",
        help="BONUS: print the actual path taken by every drone",
    )
    return parser


def main() -> int:
    """Parse arguments, run routing, and print the simulation."""
    args = build_parser().parse_args()
    visualizer = TerminalVisualizer(args.plain)
    try:
        map_data = MapParser().parse_file(args.map_file)
        route_info = Pathfinder().compute(map_data)
        simulation = Simulation(map_data, route_info.distances)
        turns = simulation.run()
        visualizer.print_map_summary(map_data)
        visualizer.print_route(
            route_info.reference_path, route_info.distances[map_data.start]
        )
        visualizer.print_turns(turns, map_data)
        if args.routes:
            visualizer.print_drone_routes(
                {drone.identifier: drone.route for drone in simulation.drones}
            )
        if args.stats:
            print("BONUS statistics:")
            for key, value in simulation.statistics(turns).items():
                print(f"  {key}: {value}")
        return 0
    except (MapParseError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
