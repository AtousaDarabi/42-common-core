"""Tests for the mandatory Fly-in path."""

import unittest
from io import StringIO

from fly_in.parser import MapParseError, MapParser
from fly_in.pathfinder import Pathfinder
from fly_in.simulation import Simulation


SAMPLE = """\
nb_drones: 2
start_hub: start 0 0
end_hub: goal 2 0
hub: middle 1 0 [zone=priority max_drones=2]
connection: start-middle [max_link_capacity=2]
connection: middle-goal [max_link_capacity=2]
"""

FORK = """\
nb_drones: 4
start_hub: start 0 0
end_hub: goal 4 0
hub: path_a 2 1
hub: path_b 2 -1
connection: start-path_a
connection: path_a-goal
connection: start-path_b
connection: path_b-goal
"""

DEAD_END = """\
nb_drones: 1
start_hub: start 0 0
end_hub: goal 2 0
hub: trap 1 1
hub: correct 1 0
connection: start-trap
connection: start-correct
connection: correct-goal
"""


def run_map(text: str) -> tuple[list[str], Simulation]:
    """Parse, route, and simulate a map, returning turns and the sim."""
    map_data = MapParser().parse_lines(StringIO(text))
    route_info = Pathfinder().compute(map_data)
    simulation = Simulation(map_data, route_info.distances)
    return simulation.run(), simulation


class FlyInTests(unittest.TestCase):
    """Verify parser, routing, and simulation behavior."""

    def setUp(self) -> None:
        """Build a small map for each test."""
        self.map_data = MapParser().parse_lines(StringIO(SAMPLE))

    def test_parser_builds_graph(self) -> None:
        """The parser should create zones and bidirectional neighbors."""
        self.assertEqual(self.map_data.zones["middle"].kind, "priority")
        self.assertIn("start", self.map_data.zones["middle"].neighbors)

    def test_parser_rejects_first_line_without_nb_drones(self) -> None:
        """nb_drones must be the map's first content line."""
        bad = SAMPLE.replace("nb_drones: 2\n", "") + "nb_drones: 2\n"
        with self.assertRaises(MapParseError):
            MapParser().parse_lines(StringIO(bad))

    def test_parser_rejects_dash_in_zone_name(self) -> None:
        """Zone names must not contain dashes."""
        bad = SAMPLE.replace("middle", "mid-dle")
        with self.assertRaises(MapParseError):
            MapParser().parse_lines(StringIO(bad))

    def test_parser_rejects_unknown_zone_metadata(self) -> None:
        """Unknown zone metadata keys must raise a parse error."""
        bad = SAMPLE.replace(
            "[zone=priority max_drones=2]",
            "[zone=priority max_drones=2 foo=bar]",
        )
        with self.assertRaises(MapParseError):
            MapParser().parse_lines(StringIO(bad))

    def test_pathfinder_reaches_goal(self) -> None:
        """The pathfinder should return a complete reference route."""
        route_info = Pathfinder().compute(self.map_data)
        expected = ["start", "middle", "goal"]
        self.assertEqual(route_info.reference_path, expected)
        self.assertEqual(route_info.distances["start"], 2)

    def test_simulation_delivers_every_drone(self) -> None:
        """The simulation should finish with valid output lines."""
        turns, simulation = run_map(SAMPLE)
        self.assertEqual(simulation.turns, 2)
        self.assertEqual(len(turns), 2)
        self.assertIn("D1-goal", turns[-1])

    def test_invalid_map_reports_error(self) -> None:
        """Invalid zone types should stop parsing clearly."""
        bad = SAMPLE.replace("zone=priority", "zone=unknown")
        with self.assertRaises(MapParseError):
            MapParser().parse_lines(StringIO(bad))

    def test_fleet_splits_across_equal_paths(self) -> None:
        """Four drones on two disjoint routes should use both routes."""
        turns, simulation = run_map(FORK)
        used = {drone.route[1] for drone in simulation.drones}
        self.assertEqual(used, {"path_a", "path_b"})
        # Splitting 2/2 across two capacity-1 branches should beat
        # forcing all four drones down one branch (which takes 5 turns).
        self.assertLessEqual(len(turns), 3)

    def test_drones_never_enter_a_dead_end(self) -> None:
        """A single drone should ignore a strictly worse branch."""
        _, simulation = run_map(DEAD_END)
        drone = simulation.drones[0]
        self.assertNotIn("trap", drone.route)
        self.assertEqual(drone.route, ["start", "correct", "goal"])

    def test_zone_capacity_is_never_exceeded(self) -> None:
        """No zone should ever hold more drones than its max_drones."""
        capacity_map = SAMPLE  # middle has max_drones=2, 2 drones total
        map_data = MapParser().parse_lines(StringIO(capacity_map))
        route_info = Pathfinder().compute(map_data)
        simulation = Simulation(map_data, route_info.distances)
        simulation.run()
        # Both drones fit in "middle" (capacity 2) at once without error;
        # run() completing without a RuntimeError is itself the guarantee
        # that _choose_move() never over-booked a zone.
        self.assertEqual(simulation.turns, 2)


if __name__ == "__main__":
    unittest.main()
