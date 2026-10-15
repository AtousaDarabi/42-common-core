"""Space-time flight planning with a shared reservation table.

Drones are planned one after another. Each drone searches for the
earliest turn at which it can reach the end zone, given everything the
previously planned drones have already reserved, and then writes its
own flight into the reservation table so later drones route around it.

Why this beats walking the static shortest path:

* A drone may take a longer route when the short one is congested,
  because what is minimised is the arrival *turn*, not the path length.
  On a fork with a 2-turn branch and a 3-turn branch this alone takes
  10 drones from 11 turns down to the optimal 7.
* Waiting is part of the search, so strategic waiting and conflict
  avoidance come for free, and deadlocks cannot happen: a drone only
  ever commits to moves that are already known to be conflict-free.

The search is Safe Interval Path Planning (SIPP, Phillips & Likhachev,
2011) driven by A*. A *safe interval* of a zone is a maximal run of
turns during which the zone still has room. Arriving earlier inside the
same safe interval is never worse (the drone can simply wait there), so
one search node per ``(zone, safe interval)`` is enough, instead of one
per ``(zone, turn)``. In practice zones are either always free or
saturated by a pipeline of drones, so a zone has one or two safe
intervals and planning stays fast even for tens of thousands of drones.
The static turns-to-goal labels from ``fly_in.pathfinder`` are exact
lower bounds, so the first time the end zone is popped its turn is the
earliest possible arrival. Among equally early arrivals, routes through
fewer non-priority zones win, as the subject asks.
"""

import heapq
from bisect import bisect_left, insort
from dataclasses import dataclass
from itertools import count
from typing import Optional

from .models import Drone, MapData, Move

NEVER = 1 << 62
"""A turn number larger than any real one ("this never happens")."""


class TimeSlots:
    """Per-turn usage counter for one zone or connection.

    Besides ``count < capacity`` checks, it answers two questions in
    (amortised) near-constant time: the first turn >= t that still has
    room (a union-find "next free slot" structure) and the first turn
    >= t that is full (a sorted list).
    """

    def __init__(self, capacity: Optional[int]) -> None:
        """Create slots; ``capacity=None`` means unlimited."""
        self.capacity = capacity
        self._used: dict[int, int] = {}
        self._skip: dict[int, int] = {}
        self._full: list[int] = []

    def has_room(self, turn: int) -> bool:
        """Return whether one more drone fits during ``turn``."""
        if self.capacity is None:
            return True
        return self._used.get(turn, 0) < self.capacity

    def add(self, turn: int) -> None:
        """Book one drone during ``turn``."""
        if self.capacity is None:
            return
        used = self._used.get(turn, 0) + 1
        self._used[turn] = used
        if used == self.capacity:
            self._skip[turn] = turn + 1
            insort(self._full, turn)

    def next_free(self, turn: int) -> int:
        """Return the first turn >= ``turn`` that still has room."""
        root = turn
        while root in self._skip:
            root = self._skip[root]
        while turn != root:
            self._skip[turn], turn = root, self._skip[turn]
        return root

    def next_full(self, turn: int) -> int:
        """Return the first turn >= ``turn`` with no room, or NEVER."""
        index = bisect_left(self._full, turn)
        return self._full[index] if index < len(self._full) else NEVER


class ReservationTable:
    """Zone occupancy and connection usage for every future turn.

    With ``strict_transit`` (the default) a drone flying into a
    restricted zone holds the connection on both turns of the flight,
    including the turn it lands. Output produced this way is valid under
    either reading of the subject; the lenient reading frees the
    connection on the landing turn.
    """

    def __init__(self, map_data: MapData, strict_transit: bool = True) -> None:
        """Create an empty table for one map."""
        self.map_data = map_data
        self.strict_transit = strict_transit
        self.zones: dict[str, TimeSlots] = {
            name: TimeSlots(
                None if map_data.has_unlimited_capacity(name)
                else zone.capacity
            )
            for name, zone in map_data.zones.items()
        }
        self.links: dict[frozenset[str], TimeSlots] = {
            key: TimeSlots(connection.capacity)
            for key, connection in map_data.connections.items()
        }
        self.horizon = 0

    def reserve(self, drone: Drone) -> None:
        """Record every zone and connection a planned drone will use."""
        start = self.map_data.start
        position = start
        last_turn = 0
        landing = False
        for move in drone.moves:
            if position != start:
                for waiting_turn in range(last_turn + 1, move.turn):
                    self.zones[position].add(waiting_turn)
            if self.strict_transit or not landing:
                self.links[move.link].add(move.turn)
            if not move.in_flight:
                self.zones[move.destination].add(move.turn)
                position = move.destination
            landing = move.in_flight
            last_turn = move.turn
        self.horizon = max(self.horizon, last_turn)


_Key = tuple[str, int]
"""A search node id: (zone, first full turn ending its safe interval)."""
_Entry = tuple[int, int, int, str, int, Optional[_Key], bool]
"""Heap entry: (f, penalty, tie, zone, arrival, parent key, restricted)."""


@dataclass
class _Node:
    """A settled search node: arrival in one zone's safe interval."""

    zone: str
    arrival: int
    parent: Optional[_Key]
    restricted_hop: bool


class FlightPlanner:
    """Plan every drone's route with safe-interval A* search."""

    def __init__(
        self,
        map_data: MapData,
        distances: dict[str, int],
        strict_transit: bool = True,
    ) -> None:
        """Prepare a planner for one map and its turns-to-goal labels."""
        self.map_data = map_data
        self.distances = distances
        self.strict_transit = strict_transit
        self.table = ReservationTable(map_data, strict_transit)

    def plan_all(self) -> list[Drone]:
        """Return all drones with conflict-free flight plans."""
        drones: list[Drone] = []
        earliest_departure = 1
        for identifier in range(1, self.map_data.drone_count + 1):
            drone, earliest_departure = self._plan_drone(
                identifier, earliest_departure
            )
            self.table.reserve(drone)
            drones.append(drone)
        return drones

    def _plan_drone(
        self, identifier: int, earliest_departure: int
    ) -> tuple[Drone, int]:
        """Search the earliest arrival for one drone.

        Reservations only ever grow, so no drone can leave the start
        earlier than the previous drone could have; the departure scan
        starts there instead of at turn 1.

        Returns:
            The planned drone and the earliest turn at which it could
            leave the start (the lower bound for the next drone).
        """
        start, end = self.map_data.start, self.map_data.end
        origin = max(0, earliest_departure - 1)
        departure = self._earliest_departure(origin)
        # Waiting at the start until every reservation is over and then
        # flying the static shortest path always works, so no plan ever
        # needs to arrive later than this.
        bound = max(self.table.horizon, origin) + self.distances[start]
        sequence = count()
        heap: list[_Entry] = [
            (origin + self.distances[start], 0, next(sequence), start,
             origin, None, False)
        ]
        settled: dict[_Key, _Node] = {}
        while heap:
            _, penalty, _, zone, arrival, parent, hop = heapq.heappop(heap)
            key = (zone, self.table.zones[zone].next_full(arrival + 1))
            if key in settled:
                continue
            settled[key] = _Node(zone, arrival, parent, hop)
            if zone == end:
                drone = Drone(identifier, self._rebuild(settled, key))
                return drone, departure
            for target, reached, extra, restricted in self._successors(
                zone, arrival, bound
            ):
                heapq.heappush(
                    heap,
                    (reached + self.distances[target], penalty + extra,
                     next(sequence), target, reached, key, restricted),
                )
        raise RuntimeError(f"no flight plan found for D{identifier}")

    def _earliest_departure(self, origin: int) -> int:
        """Return the first turn after ``origin`` a drone can leave start."""
        best = NEVER
        for neighbor in self._usable_neighbors(self.map_data.start):
            for _, reached, _, restricted in self._successors_to(
                self.map_data.start, origin, NEVER, neighbor, NEVER, 1
            ):
                best = min(best, reached - 1 if restricted else reached)
        return best if best != NEVER else origin + 1

    def _usable_neighbors(self, zone: str) -> list[str]:
        """Return neighbors a drone may enter on its way to the end."""
        zones = self.map_data.zones
        return [
            name
            for name in zones[zone].neighbors
            if not zones[name].blocked
            and name != self.map_data.start
            and name in self.distances
        ]

    def _successors(
        self, zone: str, arrival: int, bound: int
    ) -> list[tuple[str, int, int, bool]]:
        """List ``(zone, arrival, penalty, restricted)`` search successors.

        The drone may stay in ``zone`` until its safe interval ends, so
        it can leave on any turn up to the first full turn after
        ``arrival``.
        """
        leave_by = self.table.zones[zone].next_full(arrival + 1)
        found: list[tuple[str, int, int, bool]] = []
        for neighbor in self._usable_neighbors(zone):
            found.extend(
                self._successors_to(
                    zone, arrival, leave_by, neighbor, bound, NEVER
                )
            )
        return found

    def _successors_to(
        self,
        zone: str,
        arrival: int,
        leave_by: int,
        neighbor: str,
        bound: int,
        limit: int,
    ) -> list[tuple[str, int, int, bool]]:
        """Earliest arrival in each safe interval of ``neighbor``.

        Args:
            zone: Zone the drone is in.
            arrival: Turn it arrived there.
            leave_by: Last turn on which it may still leave ``zone``.
            neighbor: Zone to move into.
            bound: Arrival bound for the whole flight; successors that
                cannot beat it are not generated.
            limit: Maximum number of successors to return.
        """
        target = self.map_data.zones[neighbor]
        slots = self.table.zones[neighbor]
        link = self.table.links[frozenset((zone, neighbor))]
        restricted = target.is_restricted
        penalty = 0 if target.is_priority else 1
        flight = 1 if restricted else 0
        remaining = self.distances[neighbor]
        found: list[tuple[str, int, int, bool]] = []
        depart = arrival + 1
        while len(found) < limit:
            depart = link.next_free(depart)
            if (
                restricted
                and self.strict_transit
                and not link.has_room(depart + 1)
            ):
                depart += 1
                continue
            reached = depart + flight
            if depart > leave_by or reached + remaining > bound:
                break
            if not slots.has_room(reached):
                depart = slots.next_free(reached) - flight
                continue
            found.append((neighbor, reached, penalty, restricted))
            interval_end = slots.next_full(reached + 1)
            if interval_end == NEVER:
                break
            depart = interval_end - flight
        return found

    def _rebuild(self, settled: dict[_Key, _Node], goal: _Key) -> list[Move]:
        """Turn the chain of back-pointers into an ordered move list."""
        moves: list[Move] = []
        node = settled[goal]
        while node.parent is not None:
            previous = settled[node.parent]
            here, there = previous.zone, node.zone
            moves.append(Move(node.arrival, there, here, there))
            if node.restricted_hop:
                moves.append(
                    Move(node.arrival - 1, f"{here}-{there}", here, there,
                         True)
                )
            node = previous
        moves.reverse()
        return moves
