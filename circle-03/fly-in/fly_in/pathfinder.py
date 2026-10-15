"""Static shortest-cost labeling of the map.

No graph library is used (as required by the subject): the priority
queue is Python's own ``heapq`` and the graph is just the adjacency
lists stored on ``Zone.neighbors``.

One Dijkstra run, rooted at the end zone, gives for *every* zone the
minimum number of turns a drone needs to reach the goal if the map
were empty (``RouteInfo.distances``). Those numbers are exact lower
bounds, which makes them the heuristic of the space-time planner in
``fly_in.planner``. The same run also yields one reference shortest
route, printed for the user and used as an up-front reachability check.
"""

import heapq
from dataclasses import dataclass
from itertools import count

from .models import MapData


@dataclass
class RouteInfo:
    """Routing metadata computed once before planning starts."""

    distances: dict[str, int]
    reference_path: list[str]

    @property
    def reference_cost(self) -> int:
        """Return the turn cost of the reference route."""
        return self.distances[self.reference_path[0]]


class Pathfinder:
    """Compute cost-to-goal labels without using a graph library."""

    def compute(self, map_data: MapData) -> RouteInfo:
        """Return per-zone turns-to-goal and one example shortest route.

        Moving from zone ``a`` into zone ``b`` costs ``b``'s movement
        cost, so when the search (running backwards from the goal)
        relaxes ``neighbor -> current`` it adds the cost of entering
        ``current``.

        Raises:
            ValueError: If the start or end zone is blocked, or if the
                end cannot be reached from the start.
        """
        zones = map_data.zones
        start, end = map_data.start, map_data.end
        if zones[start].blocked or zones[end].blocked:
            raise ValueError("start and end zones cannot be blocked")
        sequence = count()
        queue: list[tuple[int, int, str]] = [(0, next(sequence), end)]
        distances: dict[str, int] = {end: 0}
        settled: set[str] = set()
        while queue:
            distance, _, current = heapq.heappop(queue)
            if current in settled:
                continue
            settled.add(current)
            if current == start:
                # Drones may never re-enter the start zone, so a route
                # that passes through it is not a real route.
                continue
            step = zones[current].movement_cost
            for neighbor in zones[current].neighbors:
                if zones[neighbor].blocked or neighbor in settled:
                    continue
                new_distance = distance + step
                if new_distance < distances.get(neighbor, new_distance + 1):
                    distances[neighbor] = new_distance
                    heapq.heappush(
                        queue, (new_distance, next(sequence), neighbor)
                    )
        if start not in distances:
            raise ValueError("no route exists from start to end")
        return RouteInfo(distances, self._reference_path(map_data, distances))

    @staticmethod
    def _reference_path(
        map_data: MapData, distances: dict[str, int]
    ) -> list[str]:
        """Walk downhill from the start, preferring priority zones."""
        path = [map_data.start]
        while path[-1] != map_data.end:
            current = path[-1]
            best: tuple[int, int, str] | None = None
            for neighbor in map_data.zones[current].neighbors:
                zone = map_data.zones[neighbor]
                remaining = distances.get(neighbor)
                if remaining is None or zone.blocked:
                    continue
                if remaining + zone.movement_cost != distances[current]:
                    continue
                option = (0 if zone.is_priority else 1, remaining, neighbor)
                if best is None or option < best:
                    best = option
            if best is None:
                raise ValueError("no route exists from start to end")
            path.append(best[2])
        return path
