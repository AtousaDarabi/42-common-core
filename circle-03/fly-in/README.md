*This project has been created as part of the 42 curriculum by <login>.*

# Fly-in

## Description

Fly-in routes a fleet of drones from a start zone to an end zone through a
network of connected zones, in as few simulation turns as possible, while
respecting every movement rule of the subject: zone capacities
(`max_drones`), connection capacities (`max_link_capacity`), two-turn
flights into `restricted` zones, `blocked` zones that can never be entered,
and `priority` zones that are preferred when routes tie.

The program reads a map file, plans a conflict-free flight for every drone,
replays the plans turn by turn while re-checking every rule, and prints the
result in the subject's format (`D1-roof1 D2-corridorA`), with colors and an
optional dashboard that shows what happens in every zone.

Every provided benchmark map is solved in the minimum possible number of
turns, including the challenger map (43 turns, record to beat: 45).

## Instructions

Python 3.10 or later. The program itself only uses the standard library;
`requirements.txt` lists the development tools (`flake8`, `mypy`).

```bash
make install      # creates .venv and installs flake8 + mypy into it
make run          # runs maps/example.map with the --visual dashboard
make run MAP=maps/benchmarks/hard/02_capacity_hell.txt
make test         # unit tests
make benchmark    # turns for every subject benchmark map
make lint         # flake8 . and mypy . with the subject's flags
make lint-strict  # flake8 . and mypy . --strict
make debug        # same as run, inside pdb
make clean        # removes __pycache__ and .mypy_cache (fclean also removes .venv)
```

Running a map directly:

```bash
python3 main.py maps/example.map                # subject output format only
python3 main.py maps/example.map --visual       # dashboard
python3 main.py maps/example.map --stats        # secondary metrics
python3 main.py maps/example.map --routes       # full route of every drone
```

| Option | Effect |
|---|---|
| (none) | One line per turn, exactly the subject format. Zones are colored when writing to a terminal, plain text when piped to a file or a checker. |
| `--visual` | Zone legend, reference route, and after each turn: the occupancy of every zone as a capacity bar, the drones in flight toward restricted zones, and the number delivered. |
| `--stats` | Turns, total moves, drones moved per turn, average turns per drone, total path cost, distinct routes used. |
| `--routes` | Every drone's route and arrival turn. |
| `--plain` / `--color` | Never / always use ANSI colors. |
| `--lenient-transit` | Frees a connection on the turn a drone lands in a restricted zone (see "Movement rules"). |

Errors (unreadable file, invalid map, unreachable goal) print one clear line
starting with `Error:` on stderr, with the line number for map syntax
errors, and exit with status 1. The program never shows a traceback.

Maps in this repository:

- `maps/example.map`: the example from the subject.
- `maps/benchmarks/{easy,medium,hard,challenger}/`: the subject's benchmark maps.
- `maps/edge_cases/`: small maps for single rules (uneven fork, equal fork,
  restricted end zone, connection written backwards, blocked shortcut,
  queueing in front of a narrow bridge).
- `maps/invalid/`: one broken map per parser error.
- `maps/large/`: stress tests with 5,000 and 10,000 drones.

## Algorithm

The work is split into three steps, each in its own class.

### 1. Static turns-to-goal labels (`fly_in/pathfinder.py`)

One Dijkstra search, run backwards from the end zone, gives every zone the
minimum number of turns a drone needs from there to the goal on an empty map.
Entering a zone costs its movement cost (1, or 2 for `restricted`), blocked
zones are skipped, and paths are not allowed to pass back through the start
zone. These labels are exact lower bounds, computed once and reused by every
drone. No graph library is used: the priority queue is `heapq` and the graph
is the adjacency lists stored on each `Zone`.

### 2. Flight planning with safe intervals (`fly_in/planner.py`)

Drones are planned one at a time. A shared **reservation table** stores, for
every zone and every connection, how many drones use it in each turn. Each
new drone searches for the **earliest turn at which it can reach the end**
given everything already reserved, then reserves its own flight so later
drones route around it.

Because the search minimizes the arrival turn rather than the path length,
drones automatically spread over several routes, including longer ones when
the short one is congested. On `maps/edge_cases/uneven_fork.map` (a 2-turn
branch and a 3-turn branch, 10 drones) this gives the optimal 7 turns, where
always taking the shortest branch needs 11. Waiting is part of the search, so
strategic waiting and conflict avoidance need no special handling, and
deadlocks cannot happen: a drone only commits to moves already known to be
free.

The search is **Safe Interval Path Planning** (SIPP) driven by **A\***:

- A *safe interval* of a zone is a maximal run of turns during which the zone
  still has room. Arriving earlier inside the same safe interval is never
  worse, because the drone can wait there. So the search needs one node per
  `(zone, safe interval)` instead of one per `(zone, turn)`.
- From a node, the drone may leave on any turn before its zone fills up. For
  each neighbor, the search computes the earliest arrival in each of the
  neighbor's safe intervals, checking the connection's capacity on the turn
  of the move (and on both turns of a restricted flight).
- A\* orders nodes by `arrival + label`. The labels never overestimate, so the
  first time the end zone comes out of the queue, its arrival is the earliest
  possible. Among equally early arrivals, the route through fewer
  non-priority zones wins.
- Each zone and connection keeps a "next free turn" union-find structure and a
  sorted list of full turns, so "first turn with room" and "end of this safe
  interval" are answered in near-constant time.
- Two pruning rules keep the search small. The arrival is bounded by "wait
  at the start until every reservation is over, then fly the shortest
  route", and reservations only grow, so no drone can leave earlier than the
  previous drone could have.

### 3. Replay and validation (`fly_in/simulation.py`)

The `Simulation` engine replays all plans turn by turn, builds the output
lines, records the occupancy of every zone after each turn for the
visualizer, and independently enforces every rule: adjacency, blocked zones,
no re-entry into the start, restricted flights landing on the very next
turn, zone capacities and connection capacities. If a plan ever broke a rule
it would raise instead of printing an invalid simulation.

### Complexity and memory

- Labels: one Dijkstra, `O((V + E) log V)`.
- Planning: per drone, an A\* over `(zone, safe interval)` nodes. On the
  provided maps every zone has one or two safe intervals (it is either free
  or saturated by a pipeline of drones), so each drone costs roughly
  `O((V + E) log V)` and the fleet costs roughly `N` times that. Paths are
  never recalculated: each drone is planned exactly once, and only the
  static labels are cached and shared.
- Memory: the reservation table holds one entry per drone per turn spent
  outside the start, `O(N x route length)`.
- Measured with `time python3 main.py ...`: 5,000 drones on the ultimate
  challenge map in about 1 s, 10,000 drones on the challenger map in about
  2.6 s.

## Movement rules as implemented

- Every turn, a drone may move to an adjacent zone, start a two-turn flight
  toward a restricted zone, or wait. A drone in flight must land on the next
  turn; it is printed as `D<id>-<from>-<to>` while in flight, named in the
  direction of travel.
- After all moves of a turn, no zone holds more than `max_drones` drones
  (start and end zones are unlimited). A drone leaving a zone frees its place
  in that same turn.
- No connection carries more than `max_link_capacity` drones in one turn.
- **Restricted flights:** the subject says the drone "occupies the
  connection during transit". By default a flight holds its connection on
  both turns, including the landing turn. This is the conservative reading:
  output produced this way is valid under either interpretation. With
  `--lenient-transit` the connection is released on the landing turn
  instead, which is faster on maps made of single-capacity restricted chains
  (`medium/02_circular_loop`: 11 turns instead of 16).

## Visual representation

- **Default view:** the plain turn lines, with each destination zone painted
  in the color from its `color=` tag. Common names (red, blue, gold, ...) use
  fixed ANSI colors; any other word gets a stable 256-color code, so every
  map's own color scheme shows up. Colors are switched off automatically
  when the output is not a terminal, so redirected output is exactly the
  subject format.
- **`--visual` dashboard:** a legend of every zone with its type and
  capacity, the reference shortest route, and after each turn the moves,
  every occupied zone with a capacity bar (`hall [##.]` = 2 of 3 places
  used), the drones currently in flight, and `delivered k/N`. Bottlenecks
  are visible at a glance: a full bar that stays full turn after turn is the
  zone limiting the throughput.
- **`--routes` and `--stats`** show each drone's route and the secondary
  metrics from the subject (drones moved per turn, average turns per drone,
  total path cost).

## Performance

All runs use the default (conservative) transit rule. The lower bound is
the shortest route length plus one turn per drone through the single-drone
choke point (the start's exit or the end's entrance). Every result reaches
it, so no valid schedule can do better.

| Map | Drones | Target | Turns | Lower bound |
|---|---|---|---|---|
| easy/01_linear_path | 2 | ≤ 6 | 4 | 4 |
| easy/02_simple_fork | 3 | ≤ 6 | 5 | 5 |
| easy/03_basic_capacity | 4 | ≤ 8 | 6 | 6 |
| medium/01_dead_end_trap | 5 | ≤ 15 | 8 | 8 |
| medium/02_circular_loop | 6 | ≤ 20 | 16 | 16 |
| medium/03_priority_puzzle | 4 | ≤ 12 | 7 | 7 |
| hard/01_maze_nightmare | 8 | ≤ 45 | 14 | 14 |
| hard/02_capacity_hell | 12 | ≤ 60 | 18 | 18 |
| hard/03_ultimate_challenge | 15 | ≤ 35 | 26 | 26 |
| challenger/01_the_impossible_dream | 25 | beat 45 | 43 | 43 |

The challenger bound: only one drone per turn can enter `gate_hell1`, and the
fastest route from there takes 18 more turns, so drone 25 cannot arrive
before turn 25 + 18 = 43. (The `maps/benchmarks/README.md` from the subject
mentions a record of 41, which is below this bound under the subject's
rules; the subject itself gives 45.)

## Bonus

- **Exceptional performance:** every benchmark is at or below its target,
  and at its lower bound.
- **Challenger map:** solved in 43 turns, beating the reference record of 45.

## Tests and code quality

```bash
make test
make lint
make lint-strict
```

`tests/test_fly_in.py` contains a `ReplayChecker` that re-derives every
position, zone occupancy and connection use from the printed output alone,
without trusting the simulation engine. The tests run it on every bundled map
in both transit modes. They also cover every parser error (with line
numbers), unreadable files, blocked or unreachable goals, priority
tie-breaking, the direction of flight tokens, the benchmark targets, the
challenger's lower bound, a 2,000-drone fleet, and the CLI (exact output
format, error messages without traceback, dashboard content). `flake8` and
`mypy` (both the subject's flags and `--strict`) report no issues.

## Resources

- Python documentation: `heapq`, `bisect`, `dataclasses`, `argparse`,
  `unittest` (https://docs.python.org/3/).
- E. W. Dijkstra, "A note on two problems in connexion with graphs" (1959).
- P. Hart, N. Nilsson, B. Raphael, "A Formal Basis for the Heuristic
  Determination of Minimum Cost Paths" (A\*, 1968).
- M. Phillips, M. Likhachev, "SIPP: Safe Interval Path Planning for Dynamic
  Environments", ICRA 2011.
- D. Silver, "Cooperative Pathfinding", AIIDE 2005 (planning agents one at a
  time against a shared reservation table).
- Union-find "next free slot" structure: R. Tarjan, "Efficiency of a Good
  But Not Linear Set Union Algorithm" (1975).

### Use of AI

AI (Claude) was used to:

- review the project against the subject, run flake8/mypy, and test it on
  every map with an independent output checker;
- find and fix problems in an earlier version: a traceback on a missing
  file, a fixed 10,000-turn limit that broke large fleets, drones that only
  ever used the shortest route, a challenger result tied at 45 instead of
  beating it, and a connection that could be double-booked while a drone
  landed in a restricted zone;
- redesign the router into the reservation-table and SIPP planner described
  above, and write the tests, the extra maps and this README.

All code was then read, tested and discussed so that every part can be
explained during the peer review.
