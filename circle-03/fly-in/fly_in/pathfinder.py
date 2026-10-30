"""Shortest-cost labeling used to steer the multi-path simulation.

No graph library is used (as required by the subject): the priority
queue is Python's own ``heapq``, and the graph itself is just the
adjacency lists already stored on ``Zone.neighbors``.

The pathfinder does not hand the simulation a single fixed route.
Instead it computes, once, the cheapest possible remaining cost from
*every* zone to the end zone (``RouteInfo.distances``). The simulation
then lets each drone independently walk "downhill" through that cost
field every turn, picking whichever still-available neighbor reduces
its remaining cost the most. Because several neighbors can legitimately
tie for the cheapest remaining cost, drones naturally spread across
every equally-good route instead of being locked onto one -- the same
principle networking calls equal-cost multi-path routing.
"""

import heapq
from dataclasses import dataclass
from itertools import count

from .models import MapData


@dataclass
class RouteInfo:
    """Routing metadata computed once before the simulation starts."""

    distances: dict[str, int]
    reference_path: list[str]


class Pathfinder:
    """Compute cost-to-goal labels without using a graph library."""

    def compute(self, map_data: MapData) -> RouteInfo:
        """Return per-zone distances-to-goal and one example route.

        A single Dijkstra run rooted at the end zone gives the cost to
        reach the goal from every other zone. Because the graph is
        undirected and movement cost only depends on the zone being
        entered, that same run's predecessor table also reconstructs a
        genuine shortest start-to-end route, which doubles as an
        up-front reachability check.
        """
        end = map_data.end
        sequence = count()
        queue: list[tuple[int, int, str]] = [(0, next(sequence), end)]
        distances: dict[str, int] = {end: 0}
        previous: dict[str, str] = {}
        visited: set[str] = set()
        while queue:
            distance, _, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            for neighbor in map_data.zones[current].neighbors:
                zone = map_data.zones[neighbor]
                if zone.blocked or neighbor in visited:
                    continue
                new_distance = distance + zone.movement_cost
                if new_distance < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(
                        queue, (new_distance, next(sequence), neighbor)
                    )
        if map_data.start not in distances:
            raise ValueError("no route exists from start to end")
        return RouteInfo(distances, self._rebuild(previous, map_data.start))

    @staticmethod
    def _rebuild(previous: dict[str, str], start: str) -> list[str]:
        """Rebuild a start-to-end route from the predecessor table."""
        path = [start]
        while path[-1] in previous:
            path.append(previous[path[-1]])
        return path
