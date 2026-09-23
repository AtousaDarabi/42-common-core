"""Turn-based, capacity-aware, multi-path drone simulation.

Every drone is only told the map's cost-to-goal field (see
``fly_in.pathfinder.Pathfinder``). Each turn, every drone independently
looks at its currently reachable neighbors, throws out any that would
not reduce its remaining cost (which rules out dead ends and backward
loops for free -- a zone that does not get you closer is never worth
entering), and tries the cheapest of what is left first. If that
neighbor's zone or connection is already full this turn it falls back
to the next-cheapest option instead of just waiting, which is what
lets a fleet split itself across several equally good routes without
being told to.

This also means routes are never pre-computed and stored per drone:
there is nothing to recompute or invalidate mid-run, only the one
map-wide distance field computed once up front.
"""

from collections import defaultdict
from typing import Union

from .models import Drone, MapData


class Simulation:
    """Schedule a fleet of drones while respecting capacity limits."""

    def __init__(self, map_data: MapData, distances: dict[str, int]) -> None:
        """Create drones at the map's start zone."""
        self.map_data = map_data
        self.distances = distances
        self.drones = [
            Drone(identifier, map_data.start)
            for identifier in range(1, map_data.drone_count + 1)
        ]
        self.turns = 0

    def run(self, max_turns: int = 10000) -> list[str]:
        """Run until every drone arrives and return formatted turn lines."""
        end = self.map_data.end
        output: list[str] = []
        while not all(drone.is_delivered(end) for drone in self.drones):
            if self.turns >= max_turns:
                raise RuntimeError("simulation exceeded the turn limit")
            self.turns += 1
            moves = self._advance_turn()
            if moves:
                output.append(" ".join(moves))
        return output

    def _advance_turn(self) -> list[str]:
        """Land in-flight drones, then greedily schedule new movements.

        A drone that lands this turn has just spent its whole turn
        arriving -- it must not also get a bonus move in the same
        turn, so it is excluded from this turn's departure scheduling
        below via ``just_arrived``.
        """
        moves: list[str] = []
        just_arrived: set[int] = set()
        for drone in self.drones:
            if drone.transit_to is None:
                continue
            destination = drone.complete_transit()
            moves.append(f"D{drone.identifier}-{destination}")
            just_arrived.add(drone.identifier)

        end = self.map_data.end
        occupied = self._occupied_zones()
        reserved_links: defaultdict[frozenset[str], int] = defaultdict(int)
        reserved_destinations: defaultdict[str, int] = defaultdict(int)

        active = [
            drone
            for drone in self.drones
            if drone.transit_to is None
            and drone.identifier not in just_arrived
            and not drone.is_delivered(end)
        ]
        active.sort(
            key=lambda drone: (
                self.distances.get(drone.zone, float("inf")),
                drone.identifier,
            )
        )

        for drone in active:
            target = self._choose_move(
                drone, occupied, reserved_links, reserved_destinations
            )
            if target is None:
                continue
            destination = target
            current = drone.zone
            connection = self.map_data.connection_between(current, destination)
            zone = self.map_data.zones[destination]
            reserved_links[connection.key] += 1
            reserved_destinations[destination] += 1
            occupied[current] -= 1
            if zone.movement_cost == 2:
                drone.begin_transit(destination, connection.name())
                moves.append(f"D{drone.identifier}-{connection.name()}")
            else:
                drone.arrive(destination)
                moves.append(f"D{drone.identifier}-{destination}")
        return moves

    def _choose_move(
        self,
        drone: Drone,
        occupied: "defaultdict[str, int]",
        reserved_links: "defaultdict[frozenset[str], int]",
        reserved_destinations: "defaultdict[str, int]",
    ) -> Union[str, None]:
        """Pick the best still-available neighbor, or None to wait."""
        current = drone.zone
        current_distance = self.distances.get(current, float("inf"))
        candidates: list[tuple[int, int, str]] = []
        for neighbor in self.map_data.zones[current].neighbors:
            zone = self.map_data.zones[neighbor]
            if zone.blocked:
                continue
            neighbor_distance = self.distances.get(neighbor)
            if neighbor_distance is None:
                continue
            if neighbor_distance >= current_distance:
                continue
            tie_break = 0 if zone.is_priority else 1
            candidates.append((neighbor_distance, tie_break, neighbor))
        candidates.sort()

        for _, _, destination in candidates:
            connection = self.map_data.connection_between(current, destination)
            if reserved_links[connection.key] >= connection.capacity:
                continue
            zone = self.map_data.zones[destination]
            if destination != self.map_data.end:
                free = zone.capacity - occupied[destination]
                free -= reserved_destinations[destination]
                if free <= 0:
                    continue
            return destination
        return None

    def _occupied_zones(self) -> "defaultdict[str, int]":
        """Count drones currently occupying each zone."""
        end = self.map_data.end
        occupied: defaultdict[str, int] = defaultdict(int)
        for drone in self.drones:
            if drone.transit_to is None and not drone.is_delivered(end):
                occupied[drone.zone] += 1
        return occupied

    def statistics(self, output: list[str]) -> dict[str, Union[float, int]]:
        """Return optional performance metrics for the bonus report."""
        moved = sum(len(line.split()) for line in output)
        average = moved / self.map_data.drone_count
        distinct_routes = len({tuple(drone.route) for drone in self.drones})
        return {
            "turns": self.turns,
            "drones": self.map_data.drone_count,
            "moves": moved,
            "average_moves_per_drone": round(average, 2),
            "distinct_routes_used": distinct_routes,
        }
