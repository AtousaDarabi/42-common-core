"""Command-line entry point for the Fly-in project."""

import argparse
import os
import sys
from typing import Optional

from fly_in.parser import MapParseError, MapParser
from fly_in.pathfinder import Pathfinder
from fly_in.simulation import Simulation
from fly_in.visualizer import TerminalVisualizer


class FlyInApp:
    """Parse arguments, run the simulation and print the result."""

    @staticmethod
    def build_parser() -> argparse.ArgumentParser:
        """Create the command-line argument parser."""
        parser = argparse.ArgumentParser(
            description="Route a fleet of drones through a Fly-in map."
        )
        parser.add_argument("map_file", help="path to a Fly-in map file")
        parser.add_argument(
            "--visual",
            action="store_true",
            help="show the dashboard: zone legend, zone states after "
            "every turn, drones in flight and delivery progress",
        )
        parser.add_argument(
            "--plain", action="store_true", help="never use colors"
        )
        parser.add_argument(
            "--color",
            action="store_true",
            help="use colors even when the output is not a terminal",
        )
        parser.add_argument(
            "--stats", action="store_true", help="print performance metrics"
        )
        parser.add_argument(
            "--routes",
            action="store_true",
            help="print the full route flown by every drone",
        )
        parser.add_argument(
            "--lenient-transit",
            action="store_true",
            help="free a connection on the turn a drone lands in a "
            "restricted zone (default: it stays occupied for both turns)",
        )
        return parser

    def run(self, argv: Optional[list[str]] = None) -> int:
        """Run the program and return the process exit code."""
        args = self.build_parser().parse_args(argv)
        try:
            map_data = MapParser().parse_file(args.map_file)
            route_info = Pathfinder().compute(map_data)
            simulation = Simulation(
                map_data, route_info, not args.lenient_transit
            )
            records = simulation.run()
            use_color = not args.plain and (args.color or sys.stdout.isatty())
            view = TerminalVisualizer(map_data, use_color)
            if args.visual:
                view.print_dashboard(route_info, records)
            else:
                view.print_turns(records)
            if args.routes:
                view.print_routes(simulation.drones)
            if args.stats:
                view.print_statistics(simulation.statistics())
            sys.stdout.flush()
        except BrokenPipeError:
            # The reader (e.g. ``head``) went away: stop quietly.
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            return 0
        except KeyboardInterrupt:
            print("\ninterrupted", file=sys.stderr)
            return 130
        except (MapParseError, OSError, RuntimeError, ValueError) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        return 0


if __name__ == "__main__":
    raise SystemExit(FlyInApp().run())
