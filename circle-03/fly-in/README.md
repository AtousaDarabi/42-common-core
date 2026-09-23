*This project has been created as part of the 42 curriculum by <your-42-login>.*

# Fly-in

## Description

Fly-in is a Python 3 drone-routing simulation. It parses a map of connected
zones, computes the true cheapest turn-cost from every zone to the end zone,
and then moves a whole fleet of drones through the map turn by turn,
spreading them across every equally-good route while respecting zone and
connection capacities.

## Instructions

Python 3.10 or later is required.

```bash
make install
make test
make run
```

Run a specific map directly:

```bash
python3 main.py maps/example.map
python3 main.py maps/example.map --plain
```

Optional bonus flags:

```bash
python3 main.py maps/example.map --stats    # turn/move/route metrics
python3 main.py maps/example.map --routes   # the actual path each drone took
```

Sample maps:

- `maps/example.map` — the map from the subject.
- `maps/fork_demo.map` — a minimal map that isolates the multi-path
  requirement: two disjoint, equal-cost, capacity-1 branches. A router that
  only ever finds one path serializes all 4 drones through a single branch
  (5 turns); splitting them 2/2 finishes in 3.
- `maps/benchmarks/{easy,medium,hard,challenger}/` — the subject's own named
  benchmark categories (linear path, simple fork, dead-end trap, circular
  loop, priority puzzle, maze nightmare, capacity hell, the ultimate
  challenge, and the challenger "Impossible Dream" map).

## Mandatory implementation

- `fly_in/models.py` — the object-oriented domain model: `Zone`, `Connection`,
  `MapData`, `Drone`.
- `fly_in/parser.py` — validates that `nb_drones` is the first line, drone
  counts, hub uniqueness, coordinates, zone/connection metadata (including
  rejecting unknown metadata keys and dashes in zone names), zone types,
  capacities, comments, and duplicate connections, with line-numbered errors.
- `fly_in/pathfinder.py` — a single Dijkstra pass, rooted at the end zone,
  computes the minimum remaining turn-cost from *every* zone to the goal
  (`RouteInfo.distances`). No graph library (`networkx`, `graphlib`, ...) is
  used, only `heapq` over the adjacency lists already stored on `Zone`.
- `fly_in/simulation.py` — schedules the whole fleet turn by turn from that
  one cost field (see "Algorithm" below), applying zone capacity, connection
  capacity, restricted-zone two-turn transit, and delivery rules.
- `fly_in/visualizer.py` — colored terminal output driven by each zone's own
  `color=` metadata (see "Visual representation" below).

## Algorithm

**Routing is not a single fixed path shared by every drone.** The
pathfinder computes, once, the cheapest possible remaining cost from every
zone to the goal (`Pathfinder.compute`, one Dijkstra run, O((V+E) log V)).
That cost field is then reused for the entire run — it is never recomputed
per turn or per drone, which keeps memory and CPU cost flat regardless of
fleet size.

Every turn, each active drone independently looks at its neighboring zones,
discards any that would not strictly reduce its remaining cost (which is
also what makes it ignore dead ends and never backtrack or loop — a zone
that doesn't get you closer is never worth entering), and tries its
cheapest remaining option first (ties go to `priority` zones, per the
subject). If that option's zone or connection is already full for this
turn, it falls through to the next-cheapest option instead of just
waiting. That fallback is what makes a fleet split itself across several
equally-short routes under congestion, without ever being told to.

This is essentially equal-cost multi-path routing applied turn-by-turn.
Per turn the simulation loop does O(D · deg) work (D = active drones, deg =
average zone degree), so the whole run is roughly O(D · T · deg) for T
turns — no repeated shortest-path searches.

### Measured results

All figures below were produced by this implementation and independently
re-validated by replaying the emitted turn-by-turn output through a second,
separate checker that re-derives zone/connection occupancy from scratch
(not by trusting the simulation's own bookkeeping).

| Map | Drones | Turns | Subject target |
|---|---|---|---|
| `easy/01_linear_path` | 2 | 4 | ≤ 6 |
| `easy/02_simple_fork` | 3 | 5 | ≤ 6 |
| `easy/03_basic_capacity` | 4 | 6 | ≤ 8 |
| `medium/01_dead_end_trap` | 5 | 8 | ≤ 15 |
| `medium/02_circular_loop` | 6 | 16 | ≤ 20 |
| `medium/03_priority_puzzle` | 4 | 7 | ≤ 12 |
| `hard/01_maze_nightmare` | 8 | 14 | ≤ 45 |
| `hard/02_capacity_hell` | 12 | 18 | ≤ 60 |
| `hard/03_ultimate_challenge` | 15 | 26 | ≤ 35 |
| `challenger/01_the_impossible_dream` (bonus, ungraded) | 25 | 45 | reference: 45 |

Every mandatory benchmark is met with room to spare. The challenger map
*ties* the subject's own reference record (45 turns) rather than beating
it — an earlier version of this run showed 39 turns, but that number came
from a bug (a drone landing from a two-turn restricted transit was still
being handed a second, bonus move in that same turn) that has since been
fixed; 45 is the honest number for the current, correct implementation.
Beating the record further is explicitly optional and ungraded, so it
wasn't pursued past a correct baseline.

On `easy/02_simple_fork` specifically, only one route ends up used even
though two exist: the single-file gate leading *into* the fork (capacity 1)
is the real bottleneck, and 3 drones never queue up at the fork itself long
enough to need the second branch. `maps/fork_demo.map` is included
separately to demonstrate the actual split under real contention.

## Visual representation

The terminal visualizer reads each zone's own `color=` tag from the map
file (red, blue, gold, "rainbow", anything) and renders it with a matching
ANSI color: common names map to a fixed palette, and any other name falls
back to a stable, deterministic 256-color choice so it's still visually
distinct. This applies to the per-zone legend printed at startup and to
each drone's destination zone in the turn-by-turn log, so a map author's
own color scheme is what actually shows up, not a fixed three-color UI
palette. Use `--plain` to disable this. `--routes` additionally prints the
literal path each drone took, which is the easiest way to see the
multi-path behavior directly.

## Bonus features

- `--stats`: turn count, total moves, drone count, average moves per drone,
  and how many *distinct* routes were actually used by the fleet.
- `--routes`: the full path taken by every individual drone.
- Equal-cost multi-path routing (see "Algorithm").
- The subject's full easy/medium/hard/challenger benchmark set is bundled
  under `maps/benchmarks/` with measured results above.

## Tests and quality

```bash
make test
make lint
```

Tests cover parsing (including the new first-line, dash-in-name, and
unknown-metadata rejections), the pathfinder, basic delivery, that a fleet
actually splits across two equal-cost branches under contention, and that a
drone never enters a strictly worse (dead-end) branch. `flake8` and `mypy
--strict` both pass with zero findings.

## Resources and AI use

- Python documentation: https://docs.python.org/3/
- Python `dataclasses`: https://docs.python.org/3/library/dataclasses.html
- Python `heapq`: https://docs.python.org/3/library/heapq.html
- Python `unittest`: https://docs.python.org/3/library/unittest.html
- Dijkstra's algorithm (general reference for the shortest-cost labeling
  used by the pathfinder).
- Equal-cost multi-path routing (general networking concept that motivated
  the turn-by-turn candidate-fallback scheme in `simulation.py`).

AI was used to review an earlier version of this project against the
subject, which surfaced the core issue this version fixes: the original
pathfinder computed one single route and handed every drone the exact same
copy of it, so the fleet never actually split across multiple paths — a
map with two disjoint equal-cost branches took 5 turns instead of the
achievable 3. AI was then used to help redesign and implement the
turn-by-turn multi-path router, fix related gaps (parser validation,
zone-color visualization, a same-turn double-move bug the new routing
exposed in restricted-zone transits), extend the test suite, and write this
README. The resulting code, its behavior, and the trade-offs described
above (e.g. why `simple_fork` doesn't show a split, why the challenger
number changed from 39 to 45) must still be reviewed, understood, and
explained by the learner during peer evaluation — this file spells out
*why* each choice was made specifically so that's possible.
