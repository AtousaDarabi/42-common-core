"""Command-line entry point and discrete drone simulation."""

import heapq
import sys
from collections import defaultdict
from typing import DefaultDict

from .models import MapData, ZoneType
from .parser import MapParseError, parse_map_file

NodeUsage = DefaultDict[str, DefaultDict[int, int]]
LinkUsage = DefaultDict[int, int]
LinkMap = DefaultDict[tuple[str, str], LinkUsage]


class DroneSimulation:
    """Find a weighted path and schedule drones on its connections."""

    def __init__(self, map_data: MapData) -> None:
        self.map_data = map_data
        self.adj: DefaultDict[str, list[tuple[str, int]]] = defaultdict(list)
        self.link_caps: dict[tuple[str, str], int] = {}
        self._build_graph()

    def _build_graph(self) -> None:
        for connection in self.map_data.connections:
            first, second = connection.zone1, connection.zone2
            if self.map_data.hubs[second].zone_type != ZoneType.BLOCKED:
                self.adj[first].append((second, self._cost(second)))
            if self.map_data.hubs[first].zone_type != ZoneType.BLOCKED:
                self.adj[second].append((first, self._cost(first)))
            key = (first, second)
            if first > second:
                key = (second, first)
            self.link_caps[key] = connection.max_link_capacity

    def _cost(self, hub_name: str) -> int:
        return self.map_data.hubs[hub_name].zone_type.movement_cost

    def find_path(self) -> list[str] | None:
        """Find a lowest-cost path with Dijkstra's algorithm."""
        start, end = self.map_data.start_hub, self.map_data.end_hub
        queue: list[tuple[float, str, list[str]]] = [(0, start, [start])]
        distances: dict[str, float] = {start: 0}
        while queue:
            cost, current, path = heapq.heappop(queue)
            if current == end:
                return path
            if cost > distances[current]:
                continue
            for next_hub, move_cost in self.adj[current]:
                priority_hub = (
                    self.map_data.hubs[next_hub].zone_type == ZoneType.PRIORITY
                )
                preference = 0.9 if priority_hub else move_cost
                new_cost = cost + preference
                if new_cost < distances.get(next_hub, float("inf")):
                    distances[next_hub] = new_cost
                    heapq.heappush(
                        queue,
                        (new_cost, next_hub, path + [next_hub]),
                    )
        return None

    def run(self) -> None:
        path = self.find_path()
        if path is None:
            raise RuntimeError("no valid path from start to end")
        node_res: NodeUsage = defaultdict(lambda: defaultdict(int))
        link_res: LinkMap = defaultdict(lambda: defaultdict(int))
        output: DefaultDict[int, list[str]] = defaultdict(list)

        for drone_id in range(1, self.map_data.nb_drones + 1):
            start_turn = 1
            while True:
                turn = start_turn
                valid = True
                for first, second in zip(path, path[1:]):
                    cost = self._cost(second)
                    key = (first, second)
                    if first > second:
                        key = (second, first)
                    for tick in range(turn, turn + cost):
                        if link_res[key][tick] >= self.link_caps[key]:
                            valid = False
                            break
                    arrival = turn + cost
                    if not valid or (
                        second != self.map_data.end_hub
                        and node_res[second][arrival]
                        >= self.map_data.hubs[second].max_drones
                    ):
                        valid = False
                        break
                    turn = arrival
                if valid:
                    turn = start_turn
                    for first, second in zip(path, path[1:]):
                        cost = self._cost(second)
                        key = (first, second)
                        if first > second:
                            key = (second, first)
                        for tick in range(turn, turn + cost):
                            link_res[key][tick] += 1
                        arrival = turn + cost
                        if second != self.map_data.end_hub:
                            node_res[second][arrival] += 1
                        label = f"D{drone_id}-{second}"
                        if cost == 2:
                            label = f"D{drone_id}-{first}->{second}"
                            output[turn].append(label)
                        output[arrival].append(f"D{drone_id}-{second}")
                        turn = arrival
                    break
                start_turn += 1

        for tick in range(1, max(output) + 1):
            print(" ".join(output[tick]))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 -m fly_in.main MAP_FILE", file=sys.stderr)
        return 1
    try:
        data = parse_map_file(sys.argv[1])
        DroneSimulation(data).run()
    except (MapParseError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
