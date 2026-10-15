"""Turn-by-turn replay of the planned flights.

The planner decides *what* every drone does; the simulation engine
plays those plans back one turn at a time, produces the output lines,
records the state of every zone after each turn (for the visualizer),
and independently enforces every movement rule of the subject. If a
plan ever broke a rule (adjacency, blocked or restricted zones, zone
capacity, connection capacity, landing after exactly one in-flight
turn), the engine raises instead of printing an invalid simulation.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Union

from .models import Drone, MapData, Move
from .pathfinder import RouteInfo
from .planner import FlightPlanner


@dataclass
class TurnRecord:
    """Everything that happened in one simulation turn."""

    number: int
    moves: list[str]
    occupancy: dict[str, int]
    in_flight: list[tuple[str, str, str]] = field(default_factory=list)
    delivered: int = 0

    @property
    def line(self) -> str:
        """Return the turn in the subject's output format."""
        return " ".join(self.moves)


class Simulation:
    """Plan the fleet, then replay and validate it turn by turn."""

    def __init__(
        self,
        map_data: MapData,
        route_info: RouteInfo,
        strict_transit: bool = True,
    ) -> None:
        """Store the map, the static routing labels and the transit rule.

        Args:
            map_data: The parsed map.
            route_info: Turns-to-goal labels from the pathfinder.
            strict_transit: Whether a drone landing in a restricted zone
                still counts against the connection's capacity on its
                landing turn (see ``fly_in.planner.ReservationTable``).
        """
        self.map_data = map_data
        self.route_info = route_info
        self.strict_transit = strict_transit
        self.drones: list[Drone] = []
        self.records: list[TurnRecord] = []

    @property
    def turns(self) -> int:
        """Return the number of turns needed to deliver every drone."""
        return len(self.records)

    def run(self) -> list[TurnRecord]:
        """Plan every drone, replay the plans and return all turns."""
        planner = FlightPlanner(
            self.map_data, self.route_info.distances, self.strict_transit
        )
        self.drones = planner.plan_all()
        self.records = self._replay()
        return self.records

    def _replay(self) -> list[TurnRecord]:
        """Apply the planned moves turn by turn while checking the rules."""
        map_data = self.map_data
        by_turn: defaultdict[int, list[tuple[Drone, Move]]] = defaultdict(
            list
        )
        for drone in self.drones:
            for move in drone.moves:
                by_turn[move.turn].append((drone, move))
        last_turn = max((drone.arrival_turn for drone in self.drones),
                        default=0)
        position = {drone.identifier: map_data.start for drone in self.drones}
        flying: dict[int, Move] = {}
        occupancy: defaultdict[str, int] = defaultdict(int)
        occupancy[map_data.start] = len(self.drones)
        delivered = 0
        records: list[TurnRecord] = []
        for turn in range(1, last_turn + 1):
            link_use: defaultdict[frozenset[str], int] = defaultdict(int)
            tokens: list[str] = []
            for drone, move in by_turn.get(turn, []):
                self._check_move(drone, move, position, flying)
                tokens.append(f"{drone.label}-{move.token}")
                delivered += self._apply_move(
                    drone, move, position, flying, occupancy, link_use
                )
            for identifier, move in flying.items():
                if move.turn != turn:
                    raise RuntimeError(
                        f"turn {turn}: D{identifier} did not land after "
                        "its in-flight turn"
                    )
            self._check_capacities(turn, link_use, occupancy)
            records.append(
                TurnRecord(
                    turn,
                    tokens,
                    {zone: n for zone, n in occupancy.items() if n > 0},
                    [(f"D{i}", m.origin, m.destination)
                     for i, m in sorted(flying.items())],
                    delivered,
                )
            )
        if delivered != len(self.drones):
            raise RuntimeError("not every drone reached the end zone")
        return records

    def _apply_move(
        self,
        drone: Drone,
        move: Move,
        position: dict[int, str],
        flying: dict[int, Move],
        occupancy: defaultdict[str, int],
        link_use: defaultdict[frozenset[str], int],
    ) -> int:
        """Update positions and counters for one move.

        Returns:
            1 if the move delivers the drone to the end zone, else 0.
        """
        landing = drone.identifier in flying
        if self.strict_transit or not landing:
            link_use[move.link] += 1
        if move.in_flight:
            occupancy[move.origin] -= 1
            flying[drone.identifier] = move
            return 0
        if landing:
            del flying[drone.identifier]
        else:
            occupancy[move.origin] -= 1
        position[drone.identifier] = move.destination
        if move.destination == self.map_data.end:
            return 1
        occupancy[move.destination] += 1
        return 0

    def _check_move(
        self,
        drone: Drone,
        move: Move,
        position: dict[int, str],
        flying: dict[int, Move],
    ) -> None:
        """Raise if one move breaks a movement rule."""
        zones = self.map_data.zones
        where = f"turn {move.turn}: {drone.label}"
        if drone.identifier in flying:
            started = flying[drone.identifier]
            if move.in_flight or move.destination != started.destination:
                raise RuntimeError(
                    f"{where} must land in {started.destination}"
                )
            return
        if move.origin != position[drone.identifier]:
            raise RuntimeError(f"{where} is not in {move.origin}")
        if move.link not in self.map_data.connections:
            raise RuntimeError(f"{where} uses a missing connection")
        target = zones[move.destination]
        if target.blocked or move.destination == self.map_data.start:
            raise RuntimeError(f"{where} enters forbidden zone {target.name}")
        if target.is_restricted != move.in_flight:
            raise RuntimeError(
                f"{where} has the wrong timing for {target.name}"
            )

    def _check_capacities(
        self,
        turn: int,
        link_use: dict[frozenset[str], int],
        occupancy: dict[str, int],
    ) -> None:
        """Raise if a zone or connection is over capacity after a turn."""
        for link, used in link_use.items():
            capacity = self.map_data.connections[link].capacity
            if used > capacity:
                name = "-".join(sorted(link))
                raise RuntimeError(f"turn {turn}: connection {name} overused")
        for zone, count in occupancy.items():
            if self.map_data.has_unlimited_capacity(zone):
                continue
            if count > self.map_data.zones[zone].capacity:
                raise RuntimeError(f"turn {turn}: zone {zone} over capacity")

    def statistics(self) -> dict[str, Union[float, int]]:
        """Return the secondary metrics suggested by the subject."""
        drone_count = len(self.drones)
        moves = sum(len(record.moves) for record in self.records)
        path_cost = sum(
            self.map_data.zones[move.destination].movement_cost
            for drone in self.drones
            for move in drone.moves
            if not move.in_flight
        )
        arrival = sum(drone.arrival_turn for drone in self.drones)
        routes = {
            tuple(drone.route(self.map_data.start)) for drone in self.drones
        }
        return {
            "turns": self.turns,
            "drones": drone_count,
            "total_moves": moves,
            "average_drones_moved_per_turn": round(
                moves / max(self.turns, 1), 2
            ),
            "average_turns_per_drone": round(arrival / drone_count, 2),
            "total_path_cost": path_cost,
            "distinct_routes_used": len(routes),
        }
