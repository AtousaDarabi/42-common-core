"""Tests for Fly-in: parser, routing, simulation rules and benchmarks."""

import io
import re
import tempfile
import unittest
from collections import defaultdict
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from fly_in.models import MapData
from fly_in.parser import MapParseError, MapParser
from fly_in.pathfinder import Pathfinder
from fly_in.simulation import Simulation
from fly_in.visualizer import ColorPalette
from main import FlyInApp

ROOT = Path(__file__).resolve().parent.parent
MAPS = ROOT / "maps"

SAMPLE = """\
nb_drones: 2
start_hub: start 0 0
end_hub: goal 2 0
hub: middle 1 0 [zone=priority max_drones=2]
connection: start-middle [max_link_capacity=2]
connection: middle-goal [max_link_capacity=2]
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

BENCHMARKS = {
    "easy/01_linear_path.txt": 6,
    "easy/02_simple_fork.txt": 6,
    "easy/03_basic_capacity.txt": 8,
    "medium/01_dead_end_trap.txt": 15,
    "medium/02_circular_loop.txt": 20,
    "medium/03_priority_puzzle.txt": 12,
    "hard/01_maze_nightmare.txt": 45,
    "hard/02_capacity_hell.txt": 60,
    "hard/03_ultimate_challenge.txt": 35,
    "challenger/01_the_impossible_dream.txt": 44,
}


class ReplayChecker:
    """Re-check simulation output from scratch, trusting only the map.

    Deliberately independent from ``Simulation``: it reads the printed
    turn lines and re-derives every position, zone occupancy and
    connection use itself.
    """

    def __init__(self, map_data: MapData, strict_transit: bool = True) -> None:
        """Store the map the output belongs to."""
        self.map_data = map_data
        self.strict_transit = strict_transit
        self.adjacent: defaultdict[str, set[str]] = defaultdict(set)
        for key in map_data.connections:
            first, second = tuple(key)
            self.adjacent[first].add(second)
            self.adjacent[second].add(first)

    def errors(self, lines: list[str]) -> list[str]:
        """Return every rule violation found in the output lines."""
        data = self.map_data
        position = {d: data.start for d in range(1, data.drone_count + 1)}
        flying: dict[int, str] = {}
        delivered: set[int] = set()
        problems: list[str] = []
        for turn, line in enumerate(lines, 1):
            links: defaultdict[frozenset[str], int] = defaultdict(int)
            seen: set[int] = set()
            for token in line.split():
                match = re.fullmatch(r"D(\d+)-(\S+)", token)
                if not match:
                    problems.append(f"{turn}: bad token {token}")
                    continue
                drone, target = int(match.group(1)), match.group(2)
                if drone in seen or drone in delivered:
                    problems.append(f"{turn}: D{drone} cannot move")
                seen.add(drone)
                here = position[drone]
                if drone in flying:
                    if target != flying.pop(drone):
                        problems.append(f"{turn}: D{drone} must land")
                    if self.strict_transit:
                        links[frozenset((here, target))] += 1
                    position[drone] = target
                elif "-" in target:
                    origin, destination = target.split("-", 1)
                    zone = data.zones.get(destination)
                    if origin != here or zone is None or (
                        not zone.is_restricted
                    ):
                        problems.append(f"{turn}: bad flight {token}")
                        continue
                    flying[drone] = destination
                    links[frozenset((here, destination))] += 1
                else:
                    zone = data.zones.get(target)
                    if (
                        zone is None
                        or target not in self.adjacent[here]
                        or zone.blocked
                        or zone.is_restricted
                        or target == data.start
                    ):
                        problems.append(f"{turn}: illegal move {token}")
                        continue
                    links[frozenset((here, target))] += 1
                    position[drone] = target
                if position[drone] == data.end and drone not in flying:
                    delivered.add(drone)
            for drone in flying:
                if drone not in seen:
                    problems.append(f"{turn}: D{drone} stalled in flight")
            for key, used in links.items():
                if used > data.connections[key].capacity:
                    problems.append(f"{turn}: connection over capacity")
            occupancy: defaultdict[str, int] = defaultdict(int)
            for drone, zone_name in position.items():
                if drone not in flying and drone not in delivered:
                    occupancy[zone_name] += 1
            for zone_name, used in occupancy.items():
                if data.has_unlimited_capacity(zone_name):
                    continue
                if used > data.zones[zone_name].capacity:
                    problems.append(f"{turn}: {zone_name} over capacity")
        if len(delivered) != data.drone_count:
            problems.append("not every drone was delivered")
        return problems


def parse(text: str) -> MapData:
    """Parse a map given as a string."""
    return MapParser().parse_lines(StringIO(text))


def simulate(
    map_data: MapData, strict_transit: bool = True
) -> tuple[list[str], Simulation]:
    """Route and simulate a map, returning output lines and the sim."""
    simulation = Simulation(
        map_data, Pathfinder().compute(map_data), strict_transit
    )
    records = simulation.run()
    return [record.line for record in records], simulation


def run_cli(*argv: str) -> tuple[int, str, str]:
    """Run the command-line app and capture its exit code and output."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = FlyInApp().run(list(argv))
    return code, out.getvalue(), err.getvalue()


class ParserTests(unittest.TestCase):
    """The parser accepts valid maps and rejects every invalid one."""

    def test_builds_graph(self) -> None:
        """Zones, types and bidirectional neighbors are created."""
        map_data = parse(SAMPLE)
        self.assertEqual(map_data.zones["middle"].kind, "priority")
        self.assertIn("start", map_data.zones["middle"].neighbors)
        self.assertIn("goal", map_data.zones["middle"].neighbors)

    def test_rejects_invalid_maps_with_line_numbers(self) -> None:
        """Every malformed line is reported with its number and cause."""
        cases = [
            ("nb_drones: 2", "nb_drones: 0",
             "line 1: nb_drones must be positive"),
            ("nb_drones: 2", "nb_drones: two",
             "line 1: nb_drones must be an integer"),
            ("max_drones=2]", "max_drones=2",
             "line 4: unrecognized syntax"),
            ("zone=priority", "zone=lava", "line 4: invalid zone type"),
            ("max_drones=2]", "max_drones=0]",
             "line 4: max_drones must be positive"),
            ("start-middle", "start-nowhere",
             "line 5: connection uses undefined zone 'nowhere'"),
            ("middle-goal", "goal-goal",
             "line 6: zone 'goal' cannot connect to itself"),
            ("middle-goal [max_link_capacity=2]",
             "middle-goal [max_drones=2]",
             "line 6: unknown connection metadata"),
        ]
        for old, new, expected in cases:
            with self.subTest(new), self.assertRaises(MapParseError) as ctx:
                parse(SAMPLE.replace(old, new, 1))
            self.assertIn(expected, str(ctx.exception))

    def test_structural_errors(self) -> None:
        """Order, duplicates and hub counts are enforced."""
        bad_maps = [
            SAMPLE.replace("nb_drones: 2\n", "") + "nb_drones: 2\n",
            SAMPLE + "nb_drones: 3\n",
            SAMPLE + "hub: middle 5 5\n",
            SAMPLE + "connection: goal-middle\n",
            SAMPLE + "start_hub: other 9 9\n",
            SAMPLE.replace("end_hub", "hub"),
            SAMPLE.replace("middle", "mid-dle"),
            SAMPLE + "hub: x 1.5 2\n",
            SAMPLE + "hub: x 1 2 [color=red] junk\n",
            SAMPLE + "hub: x 1 2 [max_drones=1 max_drones=2]\n",
            SAMPLE + "hub: x 1 2 [max_drones]\n",
            SAMPLE + "teleporter: a-b\n",
            "",
        ]
        for text in bad_maps:
            with self.subTest(text=text[-40:]):
                with self.assertRaises(MapParseError):
                    parse(text)

    def test_comments_and_blank_lines_are_ignored(self) -> None:
        """Comments may appear anywhere, including after content."""
        text = "# header\n\n" + SAMPLE.replace(
            "end_hub: goal 2 0", "end_hub: goal 2 0  # the goal"
        )
        self.assertEqual(parse(text).end, "goal")

    def test_unreadable_files_raise_parse_errors(self) -> None:
        """Missing files, folders and binary files never crash."""
        with tempfile.TemporaryDirectory() as folder:
            binary = Path(folder) / "binary.map"
            binary.write_bytes(b"\xff\xfe\x00 not text")
            for path in ("/no/such/file.map", str(MAPS), str(binary)):
                with self.subTest(path), self.assertRaises(MapParseError):
                    MapParser().parse_file(path)


class RoutingTests(unittest.TestCase):
    """Static distances and the planner's routing decisions."""

    def test_distances_count_entry_costs(self) -> None:
        """Entering a restricted end zone costs two turns."""
        map_data = parse(
            "nb_drones: 1\nstart_hub: s 0 0\n"
            "end_hub: g 1 0 [zone=restricted]\nconnection: s-g\n"
        )
        info = Pathfinder().compute(map_data)
        self.assertEqual(info.reference_cost, 2)
        lines, _ = simulate(map_data)
        self.assertEqual(lines, ["D1-s-g", "D1-g"])

    def test_blocked_or_unreachable_end_is_reported(self) -> None:
        """No route, or a blocked start or end, is a clear error."""
        unreachable = SAMPLE.replace("connection: middle-goal", "#")
        blocked_end = SAMPLE.replace("end_hub: goal 2 0",
                                     "end_hub: goal 2 0 [zone=blocked]")
        blocked_mid = SAMPLE.replace("zone=priority", "zone=blocked")
        for text in (unreachable, blocked_end, blocked_mid):
            with self.subTest(text=text), self.assertRaises(ValueError):
                Pathfinder().compute(parse(text))

    def test_drones_never_enter_a_dead_end(self) -> None:
        """A single drone ignores a branch that leads nowhere."""
        _, simulation = simulate(parse(DEAD_END))
        route = simulation.drones[0].route(simulation.map_data.start)
        self.assertEqual(route, ["start", "correct", "goal"])

    def test_longer_route_is_used_when_it_is_faster(self) -> None:
        """10 drones on a 2-turn and a 3-turn branch need only 7 turns."""
        map_data = MapParser().parse_file(MAPS / "edge_cases/uneven_fork.map")
        lines, simulation = simulate(map_data)
        self.assertEqual(len(lines), 7)
        self.assertEqual(simulation.statistics()["distinct_routes_used"], 2)

    def test_priority_zone_wins_a_tie(self) -> None:
        """With two equally short routes, the priority one is taken."""
        map_data = parse(
            "nb_drones: 1\nstart_hub: s 0 0\nend_hub: g 2 0\n"
            "hub: a 1 1\nhub: p 1 -1 [zone=priority]\n"
            "connection: s-a\nconnection: a-g\n"
            "connection: s-p\nconnection: p-g\n"
        )
        lines, _ = simulate(map_data)
        self.assertEqual(lines, ["D1-p", "D1-g"])

    def test_flight_token_names_the_direction_of_travel(self) -> None:
        """In-flight tokens follow the direction of travel.

        The token reads ``<from>-<to>`` even if the map defines the
        connection the other way round.
        """
        map_data = parse(
            "nb_drones: 1\nstart_hub: s 0 0\nend_hub: g 2 0\n"
            "hub: r 1 0 [zone=restricted]\n"
            "connection: r-s\nconnection: r-g\n"
        )
        lines, _ = simulate(map_data)
        self.assertEqual(lines, ["D1-s-r", "D1-r", "D1-g"])


class SimulationTests(unittest.TestCase):
    """Every produced simulation obeys the movement rules."""

    def check(self, map_data: MapData, strict: bool = True) -> list[str]:
        """Simulate a map and assert the independent checker agrees."""
        lines, _ = simulate(map_data, strict)
        self.assertEqual(ReplayChecker(map_data, strict).errors(lines), [])
        return lines

    def test_all_bundled_maps_are_valid(self) -> None:
        """Every map in ``maps/`` produces a rule-abiding simulation."""
        paths = sorted(MAPS.glob("**/*.txt")) + sorted(MAPS.glob("*.map"))
        paths += sorted((MAPS / "edge_cases").glob("*.map"))
        self.assertGreater(len(paths), 10)
        for path in paths:
            for strict in (True, False):
                with self.subTest(map=path.name, strict=strict):
                    self.check(MapParser().parse_file(path), strict)

    def test_benchmark_targets(self) -> None:
        """Every subject benchmark meets its target (challenger < 45)."""
        for name, target in BENCHMARKS.items():
            path = MAPS / "benchmarks" / name
            with self.subTest(name):
                lines = self.check(MapParser().parse_file(path))
                self.assertLessEqual(len(lines), target)

    def test_challenger_reaches_the_lower_bound(self) -> None:
        """The challenger map is solved in its minimum of 43 turns.

        Only one drone can leave the start per turn and the best route
        from the first gate takes 18 turns: 25 + 18 = 43.
        """
        path = MAPS / "benchmarks/challenger/01_the_impossible_dream.txt"
        self.assertEqual(len(self.check(MapParser().parse_file(path))), 43)

    def test_large_fleet(self) -> None:
        """Thousands of drones are planned quickly and validly."""
        text = (MAPS / "benchmarks/hard/03_ultimate_challenge.txt").read_text()
        map_data = parse(text.replace("nb_drones: 15", "nb_drones: 2000"))
        lines = self.check(map_data)
        self.assertEqual(len(lines), 2011)

    def test_checker_catches_violations(self) -> None:
        """The independent checker really does reject bad output."""
        map_data = parse(SAMPLE.replace("max_drones=2", "max_drones=1"))
        checker = ReplayChecker(map_data)
        self.assertEqual(checker.errors(["D1-middle D2-middle",
                                         "D1-goal D2-goal"]),
                         ["1: middle over capacity"])
        self.assertTrue(checker.errors(["D1-goal", "D2-middle"]))


class InterfaceTests(unittest.TestCase):
    """The command-line program and its terminal output."""

    def test_default_output_is_exactly_the_subject_format(self) -> None:
        """Without flags, stdout holds only the turn lines."""
        code, out, _ = run_cli(str(MAPS / "example.map"))
        self.assertEqual(code, 0)
        for line in out.splitlines():
            self.assertRegex(line, r"^D\d+-\S+( D\d+-\S+)*$")

    def test_errors_are_reported_without_traceback(self) -> None:
        """Bad paths and bad maps give exit code 1 and a clear message."""
        for path in ("/no/such/file.map", str(MAPS),
                     str(MAPS / "invalid/bad_zone_type.map")):
            with self.subTest(path):
                code, out, err = run_cli(path)
                self.assertEqual(code, 1)
                self.assertEqual(out, "")
                self.assertTrue(err.startswith("Error: "))
                self.assertNotIn("Traceback", err)

    def test_visual_mode_shows_zone_states(self) -> None:
        """``--visual`` prints the legend, zone states and progress."""
        code, out, _ = run_cli(str(MAPS / "example.map"), "--visual",
                               "--stats", "--routes")
        self.assertEqual(code, 0)
        for expected in ("Zones:", "Turn   1", "delivered 5/5",
                         "Routes taken:", "average turns per drone"):
            self.assertIn(expected, out)

    def test_colors(self) -> None:
        """Named colors keep fixed codes; unknown names are stable."""
        self.assertEqual(ColorPalette.code_for("red"), "\033[91m")
        self.assertEqual(ColorPalette.code_for("GOLD"), "\033[38;5;220m")
        self.assertEqual(ColorPalette.code_for("grey"),
                         ColorPalette.code_for("gray"))
        self.assertEqual(ColorPalette.code_for("teal"),
                         ColorPalette.code_for("TEAL"))
        self.assertEqual(ColorPalette.code_for(None), "")


if __name__ == "__main__":
    unittest.main()
